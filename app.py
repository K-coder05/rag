import streamlit as st

from main import client, tools, retrieve_context, list_topics, format_records, load_bm25_corpus, load_titles, MODEL, AGENT_SYSTEM_PROMPT
from examples import EXAMPLE_QUESTIONS, load_cached_answers, normalize

MAX_ITERATIONS = 5

st.set_page_config(page_title="Startup Library", page_icon="📚")
st.title("Startup Library Assistant")


@st.cache_resource(show_spinner="Loading search index...")
def warm_up():
    # Runs once per server process, not per session/rerun. Importing main above
    # already created the Gemini, Pinecone and Anthropic clients; this builds the
    # BM25 index and topic list so the first question doesn't pay for them.
    load_bm25_corpus()
    load_titles()


warm_up()


@st.cache_resource
def cached_answers():
    return load_cached_answers()


ARCHITECTURE = """
digraph {
    rankdir=TB
    node [shape=box style="rounded,filled" fillcolor="#f0f2f6" fontname="sans-serif" fontsize=11]
    edge [fontname="sans-serif" fontsize=9]
    q [label="Question"]
    agent [label="Claude Haiku agent loop\n(picks a tool each turn, max 5)" fillcolor="#ffe8cc"]
    dense [label="Dense search\nGemini embeddings + Pinecone"]
    bm25 [label="Keyword search\nBM25"]
    rrf [label="Reciprocal Rank Fusion"]
    topics [label="list_topics\n(title index)"]
    answer [label="Answer grounded in\nretrieved context" fillcolor="#d3f9d8"]
    q -> agent
    agent -> dense [label="search_essays"]
    agent -> bm25
    dense -> rrf
    bm25 -> rrf
    agent -> topics
    rrf -> agent [label="top-k chunks"]
    topics -> agent
    agent -> answer
}
"""


def render_sidebar():
    with st.sidebar:
        st.header("How it works")
        st.markdown(
            "An agent over ~400 Paul Graham essays and YC Startup Library posts. "
            "Each turn, Claude decides whether to search the corpus or list titles, "
            "then answers only from what it retrieved."
        )
        st.graphviz_chart(ARCHITECTURE, width="stretch")

        st.subheader("Eval results")
        st.caption("18 hand-written questions (easy, multi-hop, out-of-scope, browsing), LLM-as-judge.")
        col1, col2 = st.columns(2)
        col1.metric("Overall score", "0.95", "+0.11 vs one-pass RAG")
        col2.metric("Faithfulness", "1.00")
        col1.metric("Context recall", "0.97")
        col2.metric("Tool choice", "100%")
        st.caption(
            "Agent loop vs. single-pass RAG baseline (0.84), 1000-token chunks with 150 overlap. "
            "[Full results](https://docs.google.com/spreadsheets/d/1hyEVvpAo-MYJM3A43c-CUo1Hd3xRI01FvHSbk6QdTOs/edit?gid=0#gid=0)"
        )


render_sidebar()

if "history" not in st.session_state:
    st.session_state.history = []

def search_essays_collecting_sources(sources, query, top_k=3):
    records = retrieve_context(query=query, top_k=top_k)
    sources.extend(records)
    return format_records(records)


def render_tool_trace(tool_trace):
    if not tool_trace:
        return
    with st.expander(f"Tool calls ({len(tool_trace)})"):
        for tc in tool_trace:
            st.markdown(f"**{tc['name']}**(`{tc['input']}`)")
            st.caption(f"Why: {tc['reason']}")


def render_sources(sources):
    if not sources:
        return
    with st.expander(f"Sources ({len(sources)})"):
        for i, record in enumerate(sources, start=1):
            st.markdown(f"**{i}. {record.source}**  \nscore: {record.score:.3f}")
            st.write(record.text)
            if i != len(sources):
                st.divider()


def render_message(entry):
    with st.chat_message(entry["role"]):
        st.markdown(entry["content"])
        render_tool_trace(entry.get("tool_calls", []))
        render_sources(entry.get("sources", []))


for entry in st.session_state.history:
    render_message(entry)

clicked_example = None
if not st.session_state.history:
    examples_area = st.empty()
    with examples_area.container():
        st.markdown("**Not sure what to ask? Try one of these:**")
        for i, (col, question) in enumerate(zip(st.columns(len(EXAMPLE_QUESTIONS)), EXAMPLE_QUESTIONS)):
            if col.button(question, key=f"example_{i}", width="stretch"):
                clicked_example = question

query = st.chat_input("Ask about startups, fundraising, YC...") or clicked_example
cached = cached_answers().get(normalize(query)) if query else None

if query:
    if not st.session_state.history:
        examples_area.empty()
    entry = {"role": "user", "content": query}
    st.session_state.history.append(entry)
    render_message(entry)

if cached:
    # pre-computed with `python examples.py`, so example questions answer instantly
    render_message(cached)
    st.session_state.history.append(cached)

elif query:
    messages = [{"role": "user", "content": query}]
    tool_trace = []
    sources = []
    final_text = "Sorry, I couldn't finish reasoning about this in time."

    tool_functions = {
        "search_essays": lambda **kwargs: search_essays_collecting_sources(sources, **kwargs),
        "list_topics": list_topics,
    }

    with st.chat_message("assistant"):
        status = st.status("Thinking...", expanded=True)
        answer_area = st.empty()

        for _ in range(MAX_ITERATIONS):
            response_holder = {}

            def stream_turn():
                with client.messages.stream(
                    model=MODEL,
                    max_tokens=2000,
                    tools=tools,
                    messages=messages,
                    system=AGENT_SYSTEM_PROMPT,
                ) as stream:
                    for delta in stream.text_stream:
                        yield delta
                    response_holder["response"] = stream.get_final_message()

            with status:
                turn_text = st.write_stream(stream_turn())

            response = response_holder["response"]

            if response.stop_reason != "tool_use":
                final_text = turn_text or ""
                status.update(label="Answered", state="complete", expanded=False)
                break

            reason = turn_text.strip() if turn_text else "(no explanation given)"
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                with status:
                    st.write(f"Calling **{block.name}**({block.input})")
                try:
                    output = tool_functions[block.name](**block.input)
                    is_error = False
                except Exception as e:
                    with status:
                        st.exception(e)
                    output = str(e)
                    is_error = True

                tool_trace.append({
                    "name": block.name,
                    "input": block.input,
                    "reason": reason,
                })

                tool_result = {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                }
                
                if is_error:
                    tool_result["is_error"] = True

                tool_results.append(tool_result)

            messages.append({"role": "user", "content": tool_results})
        else:
            status.update(label="Timed out", state="error", expanded=False)

        answer_area.markdown(final_text)
        render_tool_trace(tool_trace)
        render_sources(sources)

    st.session_state.history.append({
        "role": "assistant",
        "content": final_text,
        "tool_calls": tool_trace,
        "sources": sources,
    })
