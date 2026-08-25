---
title: Agents For Non-Technical Users
source: https://www.ycombinator.com/library/NN-agents-for-non-technical-users
---

About
Companies
Library
Partners
Resources
Startup Jobs
Log in
Apply
Home
›
Lightcone Podcast
›
Agents For Non-Technical Users
LIGHTCONE
Agents For Non-Technical Users
by Y Combinator
49K views
5 months ago

In this episode of The Lightcone, we talk with Mukund and Madhav Jha, the founders of Emergent - an AI platform that lets anyone build and ship production-ready software. In just eight months, users have created more than 7 million apps on Emergent, with the number doubling in just the last 45 days. We discuss how they built one of the most powerful AI coding agents, why they focused on non-technical users and what it's like building for a global audience from India.

Transcript

Mukund (guest): So I think now we are just truly seeing this unlock where people who who were like really close to problem domain expert and but have been blocked by, you know, technology barrier to sort of really express themselves are using Emergent to sort of build these things out.

Jared Friedman (host): There's just so much focus on AI is gonna replace jobs, knowledge work is going away, like what's that gonna mean for employment and civil unrest. But like no one's really talking about the fact that actually like if you have like some agency of interest and you wanna start your own business and have autonomy over your life, like You are empiring that at scale. Welcome back to another episode of The Lightcone. Unfortunately, Garry got called to jury duty and can't be here with us today. Uh, but we are really excited to be joined by Mukund and Madhav Jar. Uh they're both twin brothers and founders of Emergent, which went through YC in summer 2024. Emergent's a platform that lets anyone build and ship production-ready software using AI agents. You guys are actually one of the fastest growing companies, I believe, YC's ever funded. Um, I mean, the statistics you were telling us were mind-blowing. You have In eight months since launch, seven million apps have been built with Emergent. Walk us through this like incredible growth you're seeing actually. When did that hit a real inflection point and how did that that feel for you guys?

Mukund (guest): So we both are twin brothers. We actually uh you know started programming when we were age twelve. Both of us came to US to drop PhDs. I dropped out of the PhD program, joined Google, and Madhav went on to um was in Xenophys, then went on uh to start the deep learning team at Amazon. And uh we've been meaning to do a startup together for a long time. And um before this I was uh running a startup in India called Dunzo, which was a hyperlocal quick commerce company. Um Dunzo

Jared Friedman (host): was a big company actually, right?

Mukund (guest): It was it was really big. Uh and and we we are almost a verb in India. So when people ship things, they say Dunzo it uh and uh and I was managing a really large team of 300 engineers uh when, you know, and we have been sort of watching the deep learning field for a while and we knew an inflection point is coming. One of the things that I observed when I was running this large engineering team was that software testing was the biggest bottleneck in shipping fast. Uh so when we started looking at you know what we want to build in AI, uh that was the first idea we actually.

Jared Friedman (host): What year was this?

Mukund (guest): This was twenty three end. Okay. Yeah. And and so when we applied to YC, like we applied with this idea of automating software testing. Uh that was the first idea. In fact, we went to a lot of VCs with this idea. They thought it was too crazy. Uh, you know, and and now looking back, it it it almost looks uh funny. And So we applied to YC with this idea. And um and when we were building this testing agents, we uh realized that if you can solve for verification, which is essentially, you know, you can solve the testing part, uh, you can actually automate all of software engineering. That was sort of our key insight that like, you know, verification is the loop which sort of keeps agent running for a longer, longer period of time. And that's when we pivoted to looking at general coding agent as a space, and we uh started building uh general coding agent.

Jared Friedman (host): And this takes us into two thousand twenty four. This is two twenty

Mukund (guest): twenty twenty four. Yeah.

Jared Friedman (host): Tell us what the landscape looked like. Like how big was Lovable at this point and just

Mukund (guest): I mean, nobody had started. Lovable had not started. I think Cursor was just just getting getting getting started. Um and very, very early. Uh I think Devin had just come out, uh so so really, really early. And And we looked at this benchmark called Sweet Bench, which is essentially a benchmark. Now it's saturated, but at that point of time, like that was the benchmark where all of the coding agents were getting measured on. And we took on this challenge of uh becoming number one on that benchmark. And like we sort of packed ourselves in a room, uh, four of us, and said, okay, let's just look at this benchmark. How do we crack it? That sort of set the foundation for Emergent. And we built uh, you know, soda coding agents, which became world number one on Sweet Bench um, you know, in two months of time. And that was the time when we sort of discovered all of the fundamental truths about building with LLMs, building with agents. Your

Jared Friedman (host): intended use at this point, we're presuming engineers.

Mukund (guest): Yeah, at that point we were like purely just a research company, just building coding agents. We were not thinking about a product. There was a time when we sort of invented the multi-agent system. We invented memory. We invented like how how do we do agent-to-agent communication? How do you scale up test time compute? A lot of those things which like were sort of coming out. Like we would we would discover something and we'll see three months later something come out in the paper. Uh, you know, uh and That sort of set the foundation for for us to So

Speaker 1: we were like cloud code before cloud code was a thing.

Mukund (guest): Bunch of the paradigms like multi-agent uh orchestration, how do you use like different different routings, all of those things we we sort of discovered?

Jared Friedman (host): I definitely want to come back to that. Um I'm curious at this point in the story though. When did you sort of pivot into becoming a tool for non-technical users.

Mukund (guest): Yeah. So we actually like once we had this coding agent, uh, we actually went the enterprise route. That was the common wisdom at that point, that hey, like go to enterprise, build for enterprise. And we spent like two, three months trying to uh you know make our agents work within an enterprise. We found that it was too slow. And at the same time, we were internally started using Emergent platform to build internal tools, internal software. And at that point, you know, we saw like lovable is going like crazy, Bolt was going like crazy. Uh so we thought, hey, why don't we have this really strong coding agent? How do we sort of package it and and and bring it out in the world? And we launched a very like small beat up uh pilot uh almost uh in June uh last year, twenty uh twenty five. And that really took off. And and since then, you know, like we have been just focused on solving uh problem for non-consumers. We in fact thought a lot of technical people would use use us. But today eighty percent of users who are on the platform are non technical users with zero programming knowledge. Uh and they're building like apps that that run real businesses on top of today. So it's almost been And they're based

Jared Friedman (host): all around the world, right? Like how many countries?

Mukund (guest): So they're they're all global audience, eighty percent, um seventy, eighty percent are in US, Europe, over one ninety countries right now.

Jared Friedman (host): Something that we and have talked a bunch about at YC internally is just um how does first mover advantage versus second mover advantage play out in the AI world? Certainly something that we've noticed, like if we look at some of our companies, like Lagora enter the legal AI space after Harvey, but is like growing incredibly fast. So there was clearly that it wasn't maybe as big of a moat around being a first mover um as you traditionally think there is in software. When you guys made that sort of the pivot or the slight change in direction into non-technical users at a time where Lovable and Bolt are growing really, really quickly, how did you think about that?

Mukund (guest): There are like two two, three different different threads that I would want to pull. One essentially is that I think the the model, uh every new model generation actually is is presenting a new opportunity of looking at the world. Like for example, when we started GPT 4 was the the first model that we sort of started looking at. And at that the biggest problem that everybody was trying to solve was JSON parsing, like a structured output format. And we thought, okay, like the next model is gonna solve for it. Um, you know, like let's not s spend time on that. And I think with every new model, what's happening is that you need to to start reimagining the world. For example, like Opus is a different class of model right now. It's gonna enable extremely long horizon task. It's gonna enable like multiple agents coordinating together. And so I think like one of the advantages of starting up second, right, is that you can actually one, like learn from what is what is not working for the current competition. Right. And also I think you fundamentally start from a different starting point, right? Like where like your aperture of the world is like very different. Like you your imagination is is really big, right? And I think a and and when we we were starting um uh emergent, we realized that like a lot of the users that were going to, you know, um some of these web these these apps, they wanted to actually really build an app that works, right? And most of these were actually like really, really optimized for front end prototyping at that point. So we started fundamentally reimagining that, okay, what would world look like if you could actually ship things to production. And our key insight was that to automate all of software engineering, you will have to build a platform that replicates what best engineering team do, like code reviews, automated testing, debugging, deployment, security, hosting. So we reimagined the entire platform from ground up, saying what would an end-to-end platform look like? And the real user need was actually to ship the product, not just the front-end prototyping. I think the second thing is like how do you sort of get the distribution? Because you're coming from behind, right? So even if your product is really, really strong. Uh and fundamentally I think you'll have to enter the market with uh a really, really strong product, which is you know head and shoulder above what what what exists in the market today for people to take notice. Um we were very confident about the product and and so a lot of our focus like in early days once we sort of launched was on how do we sort of rapidly scale up distribution. Um we built out a a large influencer network. And that was our initial sort of, you know, um starting point for us. Like we use TikTok, Instagram and part of them is a bunch of influencers to really, really spread the word out. And and that sort of, you know, kickstarted the whole thing for us.

Jared Friedman (host): So to me, sort of building the influencer marketing engine is like um it's like tactics to land grab. Like were you also thinking about just focusing on personas and specific subtypes of users you wanted to go after that weren't like either weren't being targeted by Level or or others or or Emergent was a better fit for them.

Mukund (guest): I mean our our thesis was that like there are a lot of users who would want to build serious applications, right? And that was our sort of target audience. And a lot of our marketing, a lot of our initial messaging was around that. Like, hey, come and ship uh real software. What we did was like a little bit broad broad based, like marketing and and but users that um, you know, were coming to the platform that we would convert were users who actually wanted to ship a real real app uh on the platform.

Jared Friedman (host): And was that in the messaging then?

Mukund (guest): I it it was in the messaging. Yeah. So so we would say, Hey, come and build real apps. We would also use the common errors that you would see on other platform, you know, like hey, don't don't see don't face this error uh on emergent. It seems like a key insight for you. Basically, you went very hardcore in terms of being maximalist in engineering from your experience, having run large engineering teams of three hundred engineers, having worked on deep learning teams at Amazon. You really knew how to architect the systems. Can you maybe uh share a bit how you built it? One of the uh cons of all these other big products like Lil Vol or Bolt is just that it's it's difficult to get those into a fully usable. You can get to a product type very quickly. But yours you went zero to hundred percent very quickly and that takes finesse. It's almost like that twenty percent gets eighty percent effort, like the Pareto principle, but you you did more than that, the last twenty percent of that engineering to be production was a lot of work and that's a lot. Yeah, and I think like the the last mile that you mentioned, right, is is always what people neglect, that hey, you need to make sure that not not only app gets built, it also gets deployed. And this is one of the conscious reasons why we chose to build our own infra on which the agent is like running. So like we provide like uh you know cloud sandboxes. Uh we don't outsource it to like some third-party sandbox provider, which was also pretty popular at that time, right? So we we built our own Kubernetes uh tech stack from ground up. uh the container tech stack. And one of the insights here is that if you give your uh agents the same infra during the build time and the same infra during the deploy time, then the sort of like during this like deployment phase, you don't uh encounter those many problems, right? And the fact that we have our own infra also allows us to give like rapid feedback to the agent. So your agent is only as good as the feedback that you provide. So we build this like sort of infra and agent like sort of co-build it together and from the uh from from day one.

Mukund (guest): And to your point, right, like uh because we we focused on, you know, sh building like uh ship ready apps which which are production ready, which has which comes with back end and and front end and everything. The tech stack we chose was also pretty unique to us. We have a Python backend uh server, we have a React front end server. Like most people would like typically go with like a much more like, you know, node node focused, node heavy uh tech stack, right? And and this like server client architecture where you can have like background jobs if you want to have background cues. So we knew that you know users who would who would use this app, their ambitions are gonna go bigger and bigger, right? Hey, I want to run a job which can like do this asynchronous video processing, you know, and they're gonna prompt it. And we wanted to support it from day one, right? And so it's the take the same tech stack on which Emergent is built, is what we expose to our end users, is what we expose to our agents, right? Uh on the agent side, we were very early on the multi-agent architecture. Uh so we knew that you want to be very frugal about your context management. So what you do is, hey, let the main agent, the driving agent, handle the main routine. But any delegated task that you want to delegate, you delegate to a subagent, be it like testing, be it like, hey, I want to do a design uh search or I want to do like, you know, integration search. Like, how do I integrate? this unique API. And along the way, when we were like finding doing all of this, we were able to figure out, okay, all the trajectories that we are generating, we can kind of aggregate over time and like sort of build in a long-term memory for the agent, which is very unique in the sense that your agent learns not just from your own session, it learns across the sessions. This is something I would say is one variant of continual learning uh that people are like uh interested in now. Uh you would have noticed that people are were interested in skills. Uh like people create like n skills and uh the uh there's a new benchmark called Skills Bench, which shows like agent with skills outperform agent without skills. Uh and interestingly, like those skills cannot be generated by agent themselves. Like if you generate those skills by agents, they don't like uh match up to the performance. So we were able to do it in a way where the skills get auto har uh you know sort of uh we are generated based on previous trajectories and we run it through a CI C D process and then add it to the long term memory. Uh so all of that like compounds for us, right? So if you if if your agent was struggling to do a calendar integration three weeks ago, uh today it is no longer struggling thanks to the uh the previous session where it was able to make it happen. So

Speaker 1: fascinating. So it learns on its own because I think one of the challenges of all these uh vibe coding app platforms is at some point the applications would get so complex that if you build it very simply you would run out of uh the context window for all the models because that seemed to be the the bottleneck. And I think you guys architected your way out. So you kinda build a lot of uh what the state of the art is now, but way back a year before.

Mukund (guest): Our coding agent is so powerful that we basically internally use it uh as a replacement for cloud code as developers, right? So we uh we are so proud of that. And uh but yet we don't want to expose that uh sort of powered tool to our end non-technical user. And so we even though we have this VS Code editor, we kind of hide it. Uh because what we have noticed is that non-technical users they even get panicked as soon as they see a diff. Uh we we we had a like a fairly technical PM in our team and uh like he doesn't like like JSON, you know, he's like, no, don't show me, you know, I I get intimidated. So building that user empathy where you have that user empathy and building that agent empathy, you also have to empathize with your agents. What is what is age what is agent feeling like, right?

Speaker 1: So we internally have a term called agent experience, right? That we measure that how like how how is agent's experience on the platform.

Jared Friedman (host): Actually a really important point I think people don't realize is you guys actually you actually started out essentially as sort of Devin cursor in like the actual like coding agent world for engineers. You just made the choice to package it up for non technical users. Absolutely. So you're sort of like moving almost in the opposite direction from like a lover board. Like you have like the power, you have all of the actual like power, you just need to simplify the user experience. Whereas they like sort of have like start with the user experience and they're gonna have to develop the power over time.

Speaker 1: Right. And I think fundamentally it's it's like unless you start from, you know, a a starting point which which uh sort of solves all of these problems along the line, the whole software development lifecycle, it's actually really hard to come from the other side and solve these problems. Because you have you'll make some architectural choices which are very hard to reverse.

Jared Friedman (host): Do you have any more? I'm really curious, like any more examples of where sort of as you were engineering the system, you just sort of just trust in the model. Like you mentioned JSON parsing, but was there anything else where you're like, let's not invest time in that, um, because like Opus four point five will will solve it?

Speaker 1: I mean some of them has has been, for example, um, you know, like library definition, some of the integrations that we have sort of built. Like, you know, we think that, you know, the next sort of models are solving for that. Similarly, like how do you generate unit tests? Some of those things that we we actually like would have heavily prompted before. And the other thing that we are very conscious of is that how do we give more and more autonomy to the models as they um the next generations come out. And the more autonomy you're able to give to the the models, the the better they perform. Like initially like our harness was very uh strict and you know like we would we would tighten it up um and and slowly like what we were observing is that as these models are getting larger and larger, more more more uh efficient, like you know, like the more control you give to the model uh decision making the better the the harness gets.

Jared Friedman (host): If we extrapolate that out or sort of like really far out, are you worried about where that sort of leaves you as a company versus the mod like the models themselves and the models get more powerful?

Mukund (guest): Yeah, I think there is this underlying current right now, right, in the industry that that, hey, like is is uh, you know, like Anthropic gonna eat everybody up. Yeah, I mean our view is that I think uh the the coding aspect is only twenty percent of the job, right? I think like taking an app to production is like really, really hard. And and I think what what matters is how closely are you working with the user, how how well do you understand their needs. And I think as the models are gonna get more and more sort of uh capable, I think the the human design is also gonna continuously growing at the same rate. So I think people are gonna want to build more complex apps uh on the platform. The other thing is that at least with our harness, we're able to extract 2030% more on top of these models. And and essentially like we can use multiple foundation models together to sort of extract more. Uh and I think we'll have to keep continuing uh you know like delivering more and more things to our users. For example, now we're thinking about like a lot of our users who have built the app now want to help with distribution, now want to help with growth, now want to help with like how do you sort of you know manage users uh and things like that. And I think for us the spectrum sort of keeps growing on that side.

Jared Friedman (host): agree with it. I mean there's there's uh another graph that I was sure shared recently is just like the number of software engineering positions available is actually going up, right? And I feel like at least internally at YC you're experiencing this. It's like the more powerful the tools get, the more ideas you get and the more work you want to do. And it just feels like everyone here is working like more hours doing more stuff. And it's just like the rate of like software that you're expected to ship per week just keeps going up and up and

Mukund (guest): up. It's accelerating.

Speaker 1: Yeah. It's a hedonistic adaptation to you know like hey oh this is more powerful now I can do more work. Yeah.

Mukund (guest): It is really uh Javon's paradox at play. And I I think there's a lot of uh concerns, it's like, oh, the software engineering jobs will be gone. It I don't think that's the case. I mean, based on everything that you're telling us and what we're experiencing I mean, I think we are we're in an expanding market, right? Like we are like l letting non-developers not be developers, right? I think you know that market is expanding. We also are internally seeing like the roles sort of combining. So like a PM, a designer, engineer Like a single person is doing i uh you know, like work of all all three to together, right? So like we have a PM who's by coding uh internally things, uh and recently like we um so we are seeing this internally right now where um a lot of the work that was done by like five, six people team can now be just done by like a single engineer or a single PM. YC's next batch is now taking applications. Got a startup in you? Apply at ycombinator.com slash apply. It's never too early, and filling out the app will level up your idea. Okay, back to the video. Could

Jared Friedman (host): we see a demo of emergent?

Speaker 1: Oh yeah, sure. Yeah. So this is how what uh emergent interface looks like. And uh I'm gonna like put a prompt where like because we were coming for this podcast, we I thought like, you know, there should be an app which lets you practice, you know, uh podcast questions, or maybe you're going to a job interview and you wanna practice questions, right? So you can build a full stack app on mob on emergent, you can build a mobile app. Our prompt engine is smart enough that once you give it a prompt, uh, it will figure out that this is talking about a mobile app. So it'll figure out like, hey, the the right agent to use is is a mobile app builder.

Jared Friedman (host): So even though you have like selected the wrong tab. Yes. It's just like, uh,

Speaker 1: the behind the scenes auto. Yeah, I got you. Right. So while while this is uh running, let me quickly also uh show you a few uh user apps. So this is by somebody based out of Illinois. Uh he's uh sort of has a business of audio video setup uh that they do like on as manually, right? So basically whatever this kind of like intake form they would have taken through spreadsheet and and other calls. They basically build this out without any uh coding background knowledge, right? Like, hey, this is the kind of A V setup I want. Um, so you you you go and you build your room and then you get you get uh it's a lead gen sort of a form. But this is a fairly full stack app. One

Jared Friedman (host): thing I noticed about that is like the design is really good. Like the icons, like it just like it looks like a well designed app. So we

Mukund (guest): we have actually spent a lot of time on like making the design is actually good. Yeah. Our our like so earlier there used to be a big trade off between design and functionality. Like if you were optimizing for design, like your functionality would would not be that strong. Uh and so we had to figure out like how do we sort of, you know, share the context in a way where design also gets better.

Speaker 1: There's another sort of person based out of Norway. He he sold his uh previous business to a PE and and realized how much lawyers have to struggle with spreadsheets and other things. So he built a CRM for lawyers. He he describes himself as like business developer. I I like the word he used. Like I'm a business developer and he he has doesn't have a programming background. So a lot of CRM related apps, we are seeing small businesses, it's your second monetization avenue, right? And so like one of the unique things to Emergent is that before the agent goes off to build things, it asks you for some clarification because agent wants to make sure that it understood your your uh requirements properly. And uh another thing is that non-technical users probably don't know the concept of API key. How do I get an open AI API key? So in this particular case, I can just say, hey, use Emergent LLM key. So you don't have to worry about getting API key from third party.

Jared Friedman (host): This feels like a good example of what you were saying. Um, 'cause this is sort of like the asked user question skill in clawed code, but you just like abstract that away. Like it's like build into the experience for someone who had no idea about

Speaker 1: Absolutely. I can be very like casual here. I can say, hey, uh the for the first one use emergent API key, rest asume good defaults and then go. This is the first time I hand off the agent. And like at this point I can just like close my laptop. We also have a mobile app, so you can like on the go keep trying to prompt agent if if agent requires a additional uh thing. Once it's done, uh you see a preview of your app.

Speaker 1: So here, for example, in this case, I can practice what is my origin story. Uh I can record uh what my origin story is, and I can keep going to, you know, various questions. Uh eventually This is

Mukund (guest): a podcast preparation app.

Speaker 1: Yeah. And then you can go ahead and revisit what answers you gave uh to your uh app. And so what we have noticed is that a lot of personal apps people use people build mobile apps, but a lot of business apps they would go and build a web app, right? So uh that's generally the tr uh trend we are seeing. The only other thing I wanted to show was Uh this is this is an actual Asana clone that our team built, like one of our QA engineers built internally. And uh so this is actual real emergent data.

Jared Friedman (host): I I'm curious what prompted that. Like was there some was there some feature that Asana was lacking or something it wasn't doing that made them say, Hey, we should just build our own?

Speaker 1: Yeah, it kind of like started off as a QA uh engineer's curiosity. He he like his first prompt, I looked at his all jobs. The first prompt was clone Jira. Okay. And then like he just kept going with that. And uh and I think the other thing is we do had do things a little bit differently. So for example, we ship like three times a day, morning, evening, night. So we kind of like built it very customized to the way we do things. Like we have a QA of uh uh involvement in in in many, many ways. Uh and definitely like we when we were using Asana, it was very uh Like even to customize it to to make it to your uh work style was not easy. And and we we are we're also saving like around like three thousand, four thousand dollars a month in subscription. This is really the

Mukund (guest): world of personal

Jared Friedman (host): software. Yeah. Has anybody actually edited the code for this? Or is it just a hundred percent built built with the merchant?

Mukund (guest): It's a hundred percent built with the merchant and and the good thing is that like if I want to add a feature, I have to just go to that uh, you know, project and just add a feature and it just starts building.

Jared Friedman (host): It's probably useful for you guys to dog boot the platform this way, because this is probably at the edge of the of the of the most complex apps people have built with Emergent. So it allows you to test what happens when people get to a very complex app

Mukund (guest): like this. So we have like a marketing team built out of complete CRM, completely built on Emergent. We are now like uh our customer support team is building customer support software uh completely built on emergent. And the power is that these are people who are closest to the problem, like who, you know, who understand the problem really, really well and are able to now build uh these apps and the speed at which we are able to ship, you know, these internal apps is like crazy.

Jared Friedman (host): How far down does it go though? I'm curious like even within the company, do you have people who want their like separate versions of like your internal Asana?

Mukund (guest): So currently like uh everybody in the company is using this this one tool right now. And and and it is collaboratively being built collaboratively, right? So like, you know, a PM can give a feature, a QA can give a feature, uh somebody from uh Harding can give a feature to to sort of build that out right now.

Jared Friedman (host): How do you think the sort of version control, like and feature flagging, all this stuff like develops in a world where anyone could just like write a couple of sentences to update the software they're using?

Mukund (guest): Yeah, so so th there is a testing testing phase, this is a deployment phase, right? So we have different versions maintained, uh right, and and s there is a primary owner of the software, like who actually manages this right now. And and so, you know, it evolves evolves like somebody will make a feature request, uh somebody will sort of build that out as an the agent will build it out and then like once it's accepted, then it'll it'll go to the release. It's

Jared Friedman (host): not managed through Git though. It's like your own workflow thing. So you

Speaker 1: can connect GitHub if you want to. Like we internally connect GitHub for our projects. Right. And uh like if non-technical developers are outside of emergent um like they actually call GitHub GitHub, right? So they they have very uh like limited uh knowledge of GitHub. And so they we we take care of like versioning on our side, even if they don't connect GitHub. To talk about how

Mukund (guest): you run your team, the way you hire must be very different. I mean, you're a very lean and small team. How do you hire for engineering? Yeah, so we we actually from from day one have been very conscious of the kind of team that we want to build. And essentially like we index on two things. One is problem solving. Like how good are you at problem solving? uh and second is ownership like we think that people who can like really take ownership uh you know like it we index on that and a lot of our early set of hires were people like you know we were we were really obsessed with like top hundred IT rankers so we had this like program going on where like I told you know our team that hey we must hire like top hundred IT rankers. Uh right now I think we have like IT rank one, IT rank twelve, uh all of those people working with us. And Lot of the initials that also came from Dunzo. So I because I was able to build like a really, really good team, we were able to get some some initial folks from that. The focus that that we have is is essentially like one or two people doing work of what a company would be doing. For example, our deployment, which almost mirrors what what WordCell would look like, is done by two people. Like our memory, like where you have like multiple startups solving for memory, is just built by one person. So I think like way like we give way more responsibility to people. And I think people are generally attracted towards harder problems that they want to solve.

Jared Friedman (host): Where is your team located?

Mukund (guest): So most of the team right now is in Bangalore, uh, an India office. Uh we have a very small office in SF, like three to five people here.

Jared Friedman (host): And you guys yourselves, you're kind of like split across both countries. Can you maybe just explain how how the setup

Speaker 1: works? Yeah, so I mean I I I live here in SF. I've been in like uh, you know, Bay Area for like last ten years.

Mukund (guest): I split half my time in SF, half my time in Bangalore, uh constantly jet lagged.

Jared Friedman (host): I think you guys are probably the most successful AI company that's sort of uh it's not fancy you came from like that it's an Indian company, but that's got like significant presence in India. Um why is that? I mean I

Mukund (guest): think it's like when I went back to India, uh, you know, after Google and I always had this thought that why is there no Google or Facebook from India? Right. So like from day zero I was thinking, you know, even though I started Asana, it was an India India focused company at that time. And when I was starting uh the second company, I always thought like, hey, there has to be, you know, like we have so much talent, we have, you know, so uh a lot of c now capital available, everything is available in India. Like why is are people not building glob truly global tech first companies from India and and that was the ambition that that we started with. And in my opinion, I think a lot of it is with, you know, like just your ambition. Like if you if you just dream big, if you're able to sort of really um think uh global from day zero. I think now because the internet is is sort of fully penetrated, people people can actually get understanding knowledge from everywhere. I think every single, you know, country has that opportunity to build for global audience. And if you have that sort of mindset, that ambition, I I I think I think lot I we'll see a lot more companies coming out of India doing the same.

Jared Friedman (host): I'm curious to hear what it's actually like sort of on the ground running this sort of like split country company where the team is mostly in India, but the product is overwhelmingly used in the US and Western Europe. It's not a product for the Indian market at all. What is it like running this company? How would it be different if you had built a normal Silicon Valley style company that was all based here?

Mukund (guest): Internally we have like really, really set really high standards, like a as a as a as a global sort of product. I mean, both in hiring, both in like the way we sort of develop product. Uh and I think us spending sort of time here also also helps. Like one of the things that we do really religiously is everybody talks to a customer once a week, twice a week. Everybody everyone in the everyone in the company, right? Uh they talk to a customer, everybody does customer support. So like we were like a really, really small engineering team, like twelve people team, and one person was always on call for customer support. It was a really hard decision for us because, you know, you're a really small team, you need to ship really fast and then move like one of your best engines out to do customer support was really hard. But I think that really, really helped us build the customer empathy from day zero. And I think given that like a lot of our distribution happens online, like, you know, like the teams are able to learn um from digital things and build for it. But I think us building that customer empathy from day zero, like talking to our users. like really help us bridge the gap uh you know uh in terms of like what our users want uh today and uh it's funny because like when we launched my first like five days I was just glued to a desk doing customer service uh support uh only and most of the customer requests were coming in in in different language like you know French, German, and because a lot of lot of the users were global. And thanks to AI like we were able to understand that, reply to that. And I think that that that uh you know like is also helping you know us bridge the gap there.

Speaker 1: Yeah. And we are hiring here in SF. So uh if anybody's, you know, interested in l uh, you know, joining uh in various positions, like be it uh res research across the board, like back end engineers, front end engineers, we are hiring here in SF and in Bangalore.

Jared Friedman (host): I'd love to go back to what we were talking about so uh regarding personalized software. And what do you think the applic implications are for SAAS in general? You know, like I get the provocative question is is SAAS dead now? I mean you guys essentially killed Asana for yourselves. Like is that bad for Asana and other SaaS companies?

Mukund (guest): I mean I definitely think that like the current um way uh the SAAS is existing today needs to change, right? I think like I feel there are two like sort of massive headwinds. One is more and more of these SaaS workflows are gonna get consumed by an agent, right? Like so like um you know, i uh unless your SaaS company pivots into like an agent first company, uh, you know, I th I think uh that's going to be uh hard to sort of survive. And second headwind is obviously like, you know, like people would want more and more customized software, like which they can build on Emergent, just like we built um, you know, um our own do-it uh project management tool. And we are seeing a lot of these people um, you know, building these internal tools, uh, these software uh on on platform like Arts. And like I feel the nature of software itself is changing. I think a lot more software will become agentic in nature. Um a lot of people who are building on Emergent today, like roughly twenty percent of them are actually agent tick apps. So people are actually, you know, embedding our own emergent agent inside those apps to sort of uh power you know, power a bunch of the workflows.

Jared Friedman (host): Did you have some interesting that's sounds really cool. Any interesting examples of people doing

Mukund (guest): like the uh uh app that Mary was just showing, uh, you know, the uh CRM for uh lawyers, that is an agent tick app where you know an agent can take a workflow and and run run through the process. The software itself is now morphing into, you know, agent tick. Like a lot of a lot of people would just want to, you know, build agents that can actually just do you know, a lot lot lot more of the work uh on its own. Where do you think this goes as uh agents, uh horizon for tasks gets longer and longer? I mean one of the the meter chart yeah chart is one of the ones that was very shocking recently. Yeah, I think that's the chart of the year, I would say, right? Like the the meters uh exponential growth and and like four four point five was at like I think four hours and four point six is at ten hours. Uh and we are internally sort of now like, you know, experimenting with agent swarms where agents can actually like work uh for a much longer horizon and multiple agents can sort of coordinate on a single task. Um early results are like pretty, pretty exciting. Um, you know, we'll see. I think I think by the end of the year you'll have, you know, agents which are running twenty four hours uh and like maybe hundreds of agents collaborating on this single task. Um and that's where that's where we sort of see the future going right now. How are you building for that? People's

Jared Friedman (host): How do you think about sort of movement in the opposite direction? I mean, we talked about sort of like the models themselves maybe getting more powerful and what does that mean for everyone building on top of them? But how about uh at least some of the model companies are explicitly trying to build applications and own the application layer themselves? If one of those companies decides like, you know, clawed code for non-technical users is a really valuable application to build. What implications does that have for you?

Mukund (guest): Eventually eventually I think like uh do you understand your customer's requirement really really well? Are you building closer to them? I think I think all of those fundamentals of like startup building remains the same. And I think, you know, like for us, like as long as we are focused on like really, really understanding our users need really best, I think, you know, we'll we'll compete on the project.

Jared Friedman (host): Do you think I mean maybe d do you think about all the model companies as like the same or the differences between them?

Mukund (guest): If you look at the models themselves, right? Like they're very different. Like for example, you know, um Opus is obviously a workhorse. Um, you know, like um Codex is really good in back end debugging, uh Gemini is really good in fun front end. So I think all of these models have their own behaviors and and and one of the like a good thing for us is that we can actually utilize these uh spikes that model have, like to to provide the best experience to the user. Um and I think eventually, like at least my worldview is that most of these models are gonna get get really, really commoditized, like where all of these models will have similar behaviors. Uh they'll have, you know, price price competitiveness um between them and and you can already see like, you know, like open source is like maybe three to six months behind, right? And and there's enough optionality for us to sort of really, really build the layer on top where we really meet the user where they are and and sort of support them in in sort of their their journey. Who understands the customer needs really, really well and and is able to build for that is is going to sort of win the space.

Jared Friedman (host): Users have built seven million apps with a merchant. What are all these apps? Who who are the users and what surprised you seeing what people do with it?

Mukund (guest): The users who are coming to platform for us are generally people who want to build a serious app, people who like really, really have a business use case that they want to automate or they have a business idea that they want to launch. Primary users who are coming to us are small, medium business owners. They're running their business today on email, WhatsApp, spreadsheet, uh, and would have gone to a dev shop to sort of build a custom software um to run and automate their business. They're coming to us. And if you look at the price point that, you know, we are bringing down, it would have costed you like $500,000 to build the software. Now you can build it for $5,000. completely on your own. Um and uh that is the kind of you know like unlock that we are sort of uh bringing to the world right now. Uh second, for example, this morning I was talking to a user Christy. She's based out of Alaska. Uh and she built this she's a clinical psychologist. Uh she's also uh a sports coach for Equestrian, the horse riding. And she wanted to m marry these two fields. Like, you know, like that. She has a lot of insights on psychology side. She has a lot of insight on on uh horse riding side and and she said she looked around everywhere to find an app that does that and she couldn't find one so she wanted to build one. She actually went to a dev shop.

Jared Friedman (host): Definitely the intersection of where Nietzsche is.

Mukund (guest): Yeah and and and she went to a dev shop in Nova Scotia and tried to find somebody who can build it. Uh they were charging her a bomb so she you know discovered Emergent started building uh out and she she just launched her app like a couple of weeks back. It's called Equimind on uh an App Store. Uh and it actually marries, you know, like her insights in psychology and and and uh into this this uh sports coaching. Um she has like hundreds of users right now using the using the platform. And I think that is an analog that we're trying to build. Like you know people who would have been um who have had an idea for a long time, people who are like really, really domain expert, very close to a problem, can now go and build build things up. We also have like a lot of solopreneurs building on the platform like who would have had to go and hire a technical CTO to build these apps. And the success that we are seeing on the platform is like recently somebody pinged me that hey, like this company has raised like four million dollars on an app that was built on Emergent. Really? Yeah, yeah. And and I need to get their permission to to share more. But yeah. And so I think now we are just truly seeing this unlock where people who who were like really close to problem domain expert and but have been blocked by you know technology barrier to sort of really express themselves are are are you know like using Emergent to sort of build these things out.

Speaker 1: ambitions are increasing, right? Like and so like we we want to like give agents more autonomy, right? And so like the the main thing is to make sure that the trajectory doesn't get derailed. So you always want to have like an overseeing agent, right? Like so it's like let's say a few agents are collaborating, and there is an overseeing agent as well, which is like parallelly like monitoring the overall task, right? So so we are experimenting with many different architectures, right? Like something even as simple as like just uh you know, you would have heard of this Ralph Wiggum loop kind of a phenomena, right? Like so the idea that, hey, like just keep poking the agent, hey, continue until it's done. And all of that is only possible if there is a good verification loop, right? So it comes back to, hey, Are you able to give autonomous verification feedback to the agent? Like was the job done? So a lot of our work in 10D right now is in fact still going on on building b best verifiers. There we are actually uh doing some custom fine-tuning as well. So uh we are very careful about like not directly competing with the models in the sense that we don't want to like build a Opus 4.5 alternative right away, but we do want to augment it through our custom fine-tuned verification layers. Uh so some of the fun stuff we on the research side we are doing is on on that side. And also like one thing uh these people tell us that like uh it's not just about money like hey I can give money to the dev shop but a lot of lot get lost in the translation when you're trying to express your idea to the through a developer and they say hey I know what I want to build. If I could just say it out my l out loud myself, I would I would do a better job.

Speaker 1: And so the uh the Norwegian uh person I was talking about, like he said that hey, in my team, I am the only builder. I don't even bring in anybody else because I know exactly what to build. And like others focus on the business aspects of it. So this like single solo printer sort of attitude of like, I'm gonna do it myself, I have the domain expertise, nothing is lost in translation. Uh that kind of agency is what people are looking forward to with these kind of platforms. Yeah,

Jared Friedman (host): I think it's a really important story that doesn't get told enough, actually, is like what you're building is really necessary for society. Like there's just so much focus on AI is gonna replace jobs, knowledge work is going away, like what's that gonna mean for employment and civil unrest. But like no one's really talking about the fact that actually like if you have like some agency of interest and you want to start your own business and have autonomy over your life, like you are empowering that at scale. It's so cool the like amount of human creativity that you're unlocking. Like who would have thought that the thing that the world needs is an app that marries clinical psychology with horse riding? Um and in a world of limited software, that app would never have been built. But in a world of unlimited software, you can build that and seven million other apps that like nobody would have ever gotten to build up.

Mukund (guest): Yeah, before getting into the niche of niches Yeah. I

Jared Friedman (host): mean so Pete, this is like an just an extension of the trend PG wrote about a while ago, right? And so like maybe coming out of the Second World War, you had sort of like a few big companies and people like built whole careers, hopefully staying at like IBM or whatever for a couple of decades and then retire. Then the startup wave came along and it suddenly like the world becomes higher resolution. People like Ale, maybe I should start my own company or at least join a smaller company and work at multiple companies or found multiple companies. And like the next extension of that is just everybody like runs their own like business that's at the intersection of like clinical psychology and horse riding um and finds an audience and and life uh livelihood that way.

Mukund (guest): Yeah, I mean we are excited about so many ideas coming to life. Like we really want to like reduce this gap between idea and reality and and you know, r truly enable people uh to express themselves and and and really, really like have this Cambrian explosion of ideas, like which is great for YC.

Jared Friedman (host): I would argue it doesn't have to be actually. Like the whole like I think it's just really interesting, the whole like explosion of being able to start businesses that aren't like venture funded, that aren't trying to raise lots of capital, that it's just like one person like following their passions and like having control over their life. I think it's like it's really um uplifting message.

Mukund (guest): Right. And I think we're just in the early innings of this right now. Like I think I think this this exponential is going to grow and and and we'll see larger and larger, you know, projects being built on uh emergent. Yes.

Jared Friedman (host): Okay. Well that's all we have time for today. Uh Mukund Madhav, thank you so much for joining us. It was a really fascinating conversation and congratulations on all the growth and we're excited to see where things go from here.

Mukund (guest): Thank you. Thank you so much for having us.

Up next from Lightcone Podcast
23:22
The AI Agent Economy Is Here
158K views
6 months ago
Related
39:32
Andrej Karpathy: Software Is Changing (Again)
2.5M views
1 year ago
50:11
Inside Claude Code With Its Creator Boris Cherny
241K views
6 months ago
23:22
The AI Agent Economy Is Here
158K views
6 months ago
46:00
How To Get The Most Out Of Coding Agents
127K views
6 months ago
YC's essential startup advice
Y Combinator
Here is what we, at YC, consider the most important, most transformative advice for startups.
10 questions to discuss with a potential co-founder
Y Combinator
The 10 questions that we think are most important to answer when considering a potential co-founder.
Footer
Y Combinator
Make something people want.
Programs
YC Program
Startup School
Work at a Startup
Co-Founder Matching
Resources
Startup Directory
Startup Library
Investors
Demo Day
SAFE
Hacker News
Launch YC
YC Deals
Company
YC Blog
Contact
Press
People
Careers
Privacy Policy
Notice at Collection
Security
Terms of Use
Twitter
Facebook
Instagram
LinkedIn
Youtube

© 2026 Y Combinator