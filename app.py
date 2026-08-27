import streamlit as st

from main import client, tools, retrieve_context, list_topics, format_records

MODEL = "claude-haiku-4-5"
MAX_ITERATIONS = 5
SYSTEM_PROMPT = (
    "Answer only from context. Before calling a tool, state in one brief "
    "sentence why you are calling it, then call the tool."
)

st.set_page_config(page_title="Startup Library", page_icon="📚")
st.title("Startup Library Assistant")

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

query = st.chat_input("Ask about startups, fundraising, YC...")

if query:
    st.session_state.history.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

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
                    system=SYSTEM_PROMPT,
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
