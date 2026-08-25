---
title: World Models, Explained
source: https://www.ycombinator.com/library/Sm-world-models-explained
---

Why do even our best AI models need tens of thousands of examples to learn skills that a human picks up in a handful of tries? Solving this problem is one of the great open challenges in modern AI. World models, which give AI an internal simulation of its environment, are one of the most promising paths forward.
In this episode of Decoded, YC's Ankit Gupta and Francois Chaubard discuss the intuition and math behind world models, new research, and current applications in self-driving, robotics, and more.

## Transcript

Host: One of the biggest open problems in AI right now is how to solve sample efficiency. That is, how do you get models to quickly learn new tasks or skills from relatively small amounts

Guest: of training data? Humans do this incredibly well. We can learn new games, concepts, and skills, often after just a handful of tries. Our best models, on the other hand, often need tens of thousands of data points just to learn.

Host: So today we're going to discuss what many top researchers believe is the most promising path to closing that gap: world models.

Guest: We're going to discuss the motivation and math behind world models, current applications, and why this approach might be the key to unlocking AGI.

Host: You and I have talked a lot about various ways people are training models and the sample efficiency of them. Why don't we start by just defining sample efficiency and how we intuitively think about it as humans? Yeah.

Guest: So I think from my perspective, the two major problems that we haven't left to solve is intelligence per watt and intelligence per sample. Intelligence per watt is like how how many valve perplexity points we get per watt of spend. And then intelligence per sample is basically if I have one additional sample in my data set, how much more intelligent am I getting? And so if I imagine I have a new task like our RKAGI, for example, I think like really François Chollet has been on the forefront of this thinking uh and talking about intelligence as the a rate of skill acquisition versus skill acquisition. And that's very different. And so, how fast do we get uh smarter with more and more samples? And these things are incredibly poor. At at getting smarter with with fewer and fewer samples.

Host: And for context, you know, the the RKGI test sets are a really good example of cases where humans are intuitively very good at them. Most humans can intuitively solve those puzzles with some amount of thinking and effort. But our current state of the art AI systems, what people consider frontier intelligence, basically can't do them. Right.

Guest: I mean, the there we come into new problems with such inductive bias from K through 12, like all these math in school. that we've we've had um that, you know, these models are are kind of getting from the entire compressing the entire internet. Um and and so when we come in, we're not coming in tabula rasa just like bare bones. But even so that they have, you know, I don't know what percent of the internet you've read. I've read very little percent of the internet, but despite that, and having read the entire internet, it still can't really do well on and and uh generalizing to these new tasks.

Host: So now let's think about this in like the extreme cases. In the extreme case where let's say we were perfectly sample efficient. You know, we were as sample efficient as possible. What would that mean in terms of a a a model that is uh taking a set of actions in the world?

Guest: Well, I guess um the perfect sample efficiency would be zero samples. And like uh there are examples of this, and it's uh that sounds uh absurd to say, but the it and the the um example the hypothetical I'll give on this is uh imagine I had a perfect world model. then I should never go to the environment to go and collect samples to train on. And well, that can't possibly happen for us. Like, no, it actually can happen. We do it all the time. It's called Newton's second law of motion. It's like Newton mechanics, like we basically know how to like get an object from point A to point B with a rocket, um, quite easily just by following like Newton's laws of motion.

Host: Yeah, like you when when NASA plans to intercept an asteroid and is planning it, you know, years in advance and can set it off in a trajectory where it just glides to the right thing and intersects to the right point. That is an example of a perfect world model we've built, where we're then just letting that world model act. And it that that system does not need to intelligently collect new samples from the environment to decide which direction to go next. It can already it's already been pre-programmed and can perfectly do it. Yeah,

Guest: can you imagine if like we needed to collect one million training examples of like us shooting spaceships to the moon to like know how to do it? 'Cause like this complete it w it would be we definitely wouldn't have the Apollo missions, right? Um but we do have that that ability because the the real world is differentiable. And we can do something called model predictive control that we're we're gonna talk about in a little bit. Um, but even in our own brain, I was just uh uh you know thinking about this on on the drive up, but like there's so many ways that like I can basically think about the things that you are gonna say or what a VC is gonna say when I'm when I was pitching them, or what a customer might say, customer might say. Uh, and even product being having taste. What is taste is like predicting that other people are gonna like this thing. And so we've built this world model over. Years of entrepreneurship, 10 years of like getting it wrong, right? Um, that maybe Bill Gates, uh, Steve Jobs, and uh Jensen have 50 years of of, you know, world modeling experience to know what people want. And uh and and basically this is actually proven in the 1967 uh Cog Psy study uh by Richardson. They basically showed that if you take a cohort of of three different people, three groups of people, and you uh have one go practice layups in basketball and they go and they shoot. They imp they improve if for one hour they improved by like I think it was like twenty four percent or something like that. And then if you take the other one and they just blindfold them and they imagine laying up a basketball, they improve it 23%. Interesting. Against the control. I mean, that's insane. It means that we have this crazy good world model. And there's the this uh neuroscientist at Stanford named Shaw Druckmann who basically is of the view that the entire point of the growing neocortex for the and during the great cortical expansion 10 million years ago was to get better and better and better and better at world modeling. And having just like my little VLA, which we'll define of doing the neck predicting the next action is not as good as having a world model to lean on, either for training for training purposes or for test time adaptation.

Host: Yeah. What it fundamentally comes down to is, you know, we as humans, we think about our

Host: Intuitive ability to think as coming from some implicit world model we have in our heads, encoded by genetics and our ability to learn and whatever else. It seems like models can do surprisingly intelligent things despite not having an explicit world model when it comes to natural language. When they're just talking, it seems like, you know, maybe under the hood, deep inside the weight somewhere, there's some kind of implicit understanding of the world, but there isn't an explicit representation of that. But then it seems like in certain domains, especially in robotics and self-driving, as we'll talk about, that sort of breaks down. And um, you know, maybe it would be helpful now to just think a little bit about and and just sort of define some of the uh pieces of what makes it challenging in these different domains. And then we can use that to kind of build up to why it's particularly hard in things like self driving and robotics to get these types of predictive models to work. Yeah, let's

Guest: do it. So let's actually like take a step back and just talk about like control reinforcement learning and define some let's define some common terms. So typically in um we teach a a course called decision making under uncertainty, uh, which is like the main reinforcement learning course uh at Stanford. I'd like to show like a specific example of let's say I have some drone and this is my poor little. Drone here and it has some mass m and we know that that gravity g is pulling down on it and it's currently at position uh t with velocity t, which we will collectively call the state. And to be really clear, this is gonna be uh p uh x p y pz, t t, and vx, v y z.

Host: It's like the six-dimensional state vector.

Guest: And we have uh some thrust vector U that we control. And we're trying to get to some point P star and V star, which is V star is typically zero. And so you have some platform that I want this thing, this drone to land on. Yep. So this is just a control problem, right? And so uh let's say this is like and we'll go through optical or optimal optimal, yeah. Optimal control. So how would I actually solve this? So the first thing I need to know is my transition function. And so this is my state transition function, which is st plus one,

Host: given the previous,

Guest: given st and my action, which it which I control is ut. And so this is my state transition or dynamics function or a world model. This

Host: is a world model. This is like a very fundamental for for context, you know, this this equivalent to the transition function you would think about in RL in general. Exactly.

Guest: And so uh and then what I'm trying to learn is something called a policy, which is like what UT should I uh uh emit given some st. Yep. And so this is the ultimate question. What should I do? What's what action should I take given some state ST? And so uh the way that we'll we'll solve this, and luckily we have a world model that is perfect that is called Newtonian physics. Newtonian physics. This is like Newton's second law of motion, which is F equals Ma. And so we know that the position pt plus one is gonna equal pt plus uh delta t vt plus one half delta t squared. So everyone's taking uh high school uh uh high school physics. Yep. And the same thing for the velocity.

Host: Blah blah blah. Delta

Guest: T A. And then my acceleration is the sum of sum of the for sum of the forces, uh, which is gonna be my uh UT. I think I divide by the mass and g. And so that's it. And now I have my transition function. Now how do I get to a policy? And I'm gonna apply something called model predictive control or real-time model predictive control, which is like the way that SpaceX lands the rocket on uh on some platform in the ocean. And what you're gonna do is you're gonna set up your loss function, you're gonna minimize sum over all t. You have u t to infinity, and I'm gonna minimize my p star minus pt plus v star minus vt. And usually you add this little lambda U T, which is like how much energy you're exerting. Yep. And you can't have infinite thrust. So you typically will have to say ut u max thrust. Yep, that can be achieved. And so this is easily solvable with convex optimization. And so this is convex, this is convex, this is convex. The sum of convex functions is convex. This is a convex constraint. And so I DCP disciplined convex programming means that I can put this into C VXPy and it will just give me out my policy, which will be The s solution will be the optimal U T plus one all the way to

Host: infinity. So we can solve this in closed form, basically. Like you know, we we can because we have this world model of Newtonian physics, we can say at every step exactly how this drone should fly so that it lands on the appropriate thing under a set of constraints like max thrust available.

Guest: Exactly. You'll you'll run your log barrier or interior point, whatever, to some solver on this, and and it will give me uh my optimal, then this would be literally the optimal path that this thing can take to get to this state. And that will minimize and then and I can I can do increase this if I if I want it to do the least energy path, or if and I make that zero if I want it to be the fastest. And so those that's typically the way that you would do uh what I would well call like deterministic. uh um uh differentiable control. And why differentiable? Because I can take the I can form the Lagrangian by by taking this minus this constraint and uh and take the gradient of it. And I can do Robbins-Monro.

Host: You use the fact that it's differentiable to to do the the optimization.

Guest: Exactly. If this is non-differentiable, you cannot do convex optimization and you cannot do SGD. Uh uh even if it's non convex, you could still solve and get and get a pretty good solution uh as we do in deep learning. But I I you if it's non differentiable, you kinda can't. There's nothing you can do.

Host: So yeah, l let's have an example then of how you could make this nondefranchable. Like well what's a what's a scenario, I guess, even in like this drone scenario where it now becomes non-defranchable. Yeah.

Guest: So I'll put this adversary named Unkit. Okay. And uh and your job is to you have another drone, let's say, Unkit's drone is to try to hit me. And stop me from getting there.

Host: Now from the position of your drone, you don't know what actions I'm gonna take.

Guest: Right. And so now let's just call this the uh this would be now we're definitely not not deterministic, we're stochastic. Um and stochastic and non-differentiable. Yeah. And in this case. My state transition, what is ST plus one? It's going to be my state I'm in now, my thrust, and what Ankit's gonna do. Right.

Guest (host): And these it was all differentiable until this blue variable. Yeah, then

Host (host): I can't like back prop through your brain. Yeah. To tell it say what you're gonna do with your little drone controller. Yep. Right. It's cum completely uh uh non-deferentiable now. And I am resorting and I have to resort to this awful area called reinforcement learning, which is just super brutal and it's sprawling and there's so many different things, and you'll hear things like when you study initial uh um reinforcement learning called value iteration or policy iteration. Um, and there's DQN or deep Q learning or just Q learning. Yep. Um, there's actor critic, there's all this mega stuff.

Guest (host): All of this stuff ultimately comes down to ways to estimate, to, to model this non-differentiable stochastic process. Exactly.

Host (host): Yeah, and so like that's basically the the main thing is is you're gonna start talking about uh this as a model where I'm gonna introduce this psi to say that this is gonna be some model that's gonna take in these things and then output this, um, and that we're gonna train it over many, many instance instantiations of this, and that's so get a better and better world model. And then I need to train some policy A T S T. And then typically you also need a value function. Okay. And that is the value of some state. And to discern between the value of different states. And like in this case, I don't know what a valid state is, but like let's just say I was doing um uh like uh SpaceX with with um launching rockets and landing rockets in Florida. Let's just say that like there's different if I have my launch pad here and I have a whole bunch of houses here, let's just say The path going from here to here, I may think that doing this and then coming across here and burning all these houses alive may be not s high highly value. So I might say as an example, they typically call this like a some kind of a cone here. And I might say like it's low value to be here or and it's a very high value to be to be in this column or something, right?

Guest (host): In a sense, a value gives you some expectation of future rewards, like the sum of future rewards you're getting. And so if you if you're in a bad space, you would set the value to zero or negative negative infinity or something like that. Yeah.

Host (host): So so we can we can we should introduce R, R T as well. And so typically, like if you're uh playing Go or chess, like winning the game, uh, you can say winning the game is plus one, minus one for losing, draw a zero. That's what's done in AlphaGo. In chess, we have these heuristics, like a a a pawn is point is worth one point, a rook is worth five, et cetera, et cetera. So you can like l already have reward. is is the difference in in in board board state. And then this, yes, will be the sum of my discount. Should just do T of R T. Yeah. Uh given and it and it's important also to to to s use this nomenclature. um v pi. And the reason why that's important is because what it what's actually happening here is this is the discounted reward following policy pi. Correct. And so that means that when I'm in this state, I will take this action and then I'll end up in this to SC plus one. And then I'll take this action and it's it and it taking it greedy. And so that's the value with respect to pi. Yeah.

Guest (host): And so ultimately what it comes down to is we are trying to still find a new policy pi. And along the way we will use machine learning models in various capacities. This is standard RL to estimate the value function given the rewards we're receiving. Right. And then where world models come in is a way of incorporating all of those into some sort of joint modeling of the state and action distribution so that we can make more intelligent policies off of it. Right.

Host (host): And so your standard kind of setup for this is what I'm always trying to get to at the end of the day is some joint distribution, which would be st plus one given uh where I'm at now, uh where I'm at now. And then this factorizes with chain rule simply to my pi, my policy, at given st and my world model. And I'll give this. This is usually represented with theta. And this is my uh world model, which would be um st plus one given st and at. Yeah. And so and these are typically learned uh uh separately and like and like you can imagine in fact actually you can actually learn this this is a video generation model and I have the frame st and I predict the next frame S T plus one. Right. And then and we'll get into this. Yeah

Guest (host): for those of us who kind of saw our our diffusion model series often people these days use video diffusion for exactly this.

Host (host): Yeah. And then what you can do, and this is like the in vogue thing to do, since Danijar and and uh um Dream the Dreamer paper series from V1 to V four is do action conditioning later, like similar to clip, where we will inject this like input head or input tail to come into the model to uh influence and and and enable the world model to have embodiment. What does that mean? It means that not only can I predict like as a plant or tree on the on the growing on the the side of the of the building, I can like see the world go passing by, but I can I can actually influence it. And I can change the the world and I can I can learn that with AT. And that's far fewer samples uh to do this post action conditioning um if I already have a really good uh uh S T to S C plus one world model.

Guest (host): And so here you're saying, you know, what's also in vogue now is jointly training these versus separately training them.

Host (host): Exactly. And so this is called that is called a world action model, where the the some of the issues here is one, there's all these training dynamics. If these things are disparate, training on different sets and things like that. Uh the other issue is plainly obvious. What I have to do to actually do test time planning is I'll have to sample my with model one, invoke theta and then pass that sampled action into here and then roll it out to S T plus one. And it's very expensive and it's a very not real time to major issues and why like why can't we just scale up AlphaGo to like solve all the problems? Um is because it's because of this property. If I have one invocation to the model and it gives me both, here's the action I should take and here's the S T plus one that'll end up much, much cheaper, much, much

Guest (host): faster.

Guest (host): Okay, so I I think that's a really good segue. I think why don't we now motivate everything we just described through a series of increasingly complex environments? So I'll contend that I think the right set of environments for us to consider is chess followed by Go, followed by self-driving, followed by robotics.

Guest (host): Um, all right, so let's go through a couple of examples of problems that we want to apply. uh reinforcement learning too. So chess is a is a pretty easy one. There's an eight by eight grid.

Host (host): Yep.

Guest (host): Um and so typically when you when you uh approach any uh RL problem you're gonna look at uh star. And so this this the size of the state, uh uh the number of states I can be in. So if if I have these eight here and these eight, so this would be eight, sixteen, thirty-two, so it'd be thirty-two to the sixty-four.

Host (host): Yes, quite large.

Guest (host): Quite large. Then uh my transition function is. stochastic and non-differentiable because

Host (host): you can you don't know what the other player's

Guest (host): gonna do. So if I'm uh at like in uh uh playing [chess.com](http://chess.com) at my house I move and then something happens and it comes back and and then now you moved and the board has changed. So I can't really differentiate through what the other player uh is is doing. The cardinal action space is actually quite small. Um, even though there's 32 uh uh pieces and all that stuff, the there's only eight possible moves in expectation that you can actually that are legit moves. So like

Host (host): in any in any given uh state, there's only eight-ish moves you could do.

Guest (host): Let's just say in the beginning I can move all my pawns, I can move my horses. So that's ten. Yeah. That's like not that much. So this is extremely small. And then my reward, we can use the heuristic based approach, or we can just say, you know, plus one, zero, or minus one if I lose, plus one if I win. And uh so this is very tractable.

Host (host): You say it's tractable even though there's a really big state space here. Yeah. But why don't we talk about that for just a second? I think this is a really important point. And when you say it's tractable, you're specifically referring to the action space being small because it affects the kind of like combinatorial expansion here. Should we talk about that for just a second? Yeah. Or maybe we can add go and then kind of contrast the two.

Guest (host): Yeah, so but why don't we do that? Because um it's the because I want to get to the AlphaGo uh um the way that they solve this. And you're right. So if I were to do this naively and I just took um I'm at SC plus one and I want to do look aheads. Uh what I would do is I would take all of the actions I can take. So there's eight. So I would do action one, action two, action eight. Bop bop bop. And then each one of these I need to exp expand it for all possible states. And so now I need to do cardinality S, which we just said is this huge friggin' number. And so I have to do that eight times. And then I have to do it again. I have to do it again. So just doing looking forward one move is like Quite interactable. Al

Host (host): although at the same time, you know, the you everyone starts at the same starting position. And while it is a really large space, you know, it there isn't an infinity number of potential there's actually a really small number of game boards even four moves into the game. Right. As opposed to a game where you could start in any permutation, for example, of initial game state and put a few states down.

Guest (host): Yeah, so so this is like definitely over uh um done. 'Cause it there's there's it's it's much, much less than this in practice. Yes. But just naively like looking at, you know, uh uh what uh possible game states could be uh as a rough math here but this is roughly the idea and then each one of these leaves i need to invoke my value function right uh which is the value of that state t plus one and so i have to do that all many times and we'll get this well off we go but like this ends up being estimating the leaf node uh because what at the end of the day my policy A T S T, I want to pick, I want the argmax of like the value of the the following the

Host (host): arg max action, I guess it'd be

Guest (host): an A here. A, exactly, yeah. The argmax over A of the value of the state of the of the N state, S T plus N, let's say. It's like that's the the main goal here. Um and so for me to do that, I need to like roll all this out, estimate the value, and then pick the the best one. And so this this quickly grows. Um however. And we'll we'll see this about how we go, which is actually ha actually has an even bigger state space. Um, so I think it's nineteen by nineteen. Um parametron off. I don't think it's spot right now. So yeah, this nineteen by nineteen grid. You can in each one it can be black, white, or or nothing there. Mm-hmm. So I have three. Uh so let's do our star again. So the cardinality of the state, I think, is gonna be s uh two or three, my ternary thing here. The nineteen squared. I think it's three sixty one. Yeah, something like that. 361. Um my transition, same issue. I don't know. Uh my action space is gonna be 361, let's say.

Host (host): So it's a good amount bigger than chess. Much bigger. But it's still not uh enormous. Yeah. As we'll see in a second.

Guest (host): Yeah. And so basically what they do, they call this Z, which is kind of annoying, but let's just call it R. And it's the terminal state. It's the terminal when they won the game. And they basically, you know, you have your trajectory, which is um S zero A zero R zero. Um Then all the way to the end of the game. Yep. S N A N R N. And if you won, then all of these, uh all the moves that black if black won, all the moves that black did get plus, all the moves that white did were minus one. And they just that's how they create their um their rollouts.

Host (host): Rollout refers to a taking N steps of play of all players, one after another. Yeah. of moves under a specific policy at the at the particular instantiation of

Guest (host): it. Right. So let's just sit let's probably under this policy P theta T. Yeah. And we're gonna overload T, but like this is that instantiation. We froze that model. We froze that model and we play, I think it's like 70 games. And we like treat all those, and we said we're gonna subsample a bunch of um of these uh state action results, state action results to train our to update our policy in our our um in our world model, our transition model. And what it's actually doing is we we take in an ST, we give it set to some theta, and it wants to output um the probability of st plus one being played. uh which is our transition function and uh the uh value of the current

Host (host): state. And how do we get the value?

Guest (host): And so the value of the current state, uh well, both of them are coming out of out of the model, but basically the loss function L

Guest (host): Theta is going to equal, and it's going to be early close to this uh control problem one. Is we have some v theta minus this z, which we'll just call it r here, um squared, and then plus uh actually sorry, it's minus this pi, which I'll explain in a second, log p theta. And I think they everyone includes this, but they include it in the paper. So I'll include it there as well, which is the um weight decay. Yep. And so um so this is basically uh what uh our loss function is. Then we'll play a bunch of these games and let's try to be a little bit organized here. And uh and so this is our setup, this is our architecture. And now the most once we train this thing, we do an insane ex insanely expensive task of uh of test time planning. Yeah. And so this trend in RL is just called test time

Host (host): planning. And the and the specific algorithm they use here for this is Monte Carlo

Guest (host): Tree Search. MCTS. And so this is one of the possible things that you could do. It ends up working extremely well if you have small action spaces.

Host (host): Yeah, so let's let's just like very intuitively talk about what MCTS does. And a lot of people have heard about Monte Carlo Tree Search because AlphaGo was such a you know big moment. But how exactly does that map into our star and value function and policy?

Guest (host): Yep. So I'll take this ST. This will give me uh 361 uh uh uh numbers that sum to one. And so I'll have some probability of uh of where these things are gonna go for the of where my my opponent will play. Um here.

Host (host): So these are like the sets of actions. Yeah.

Guest (host): So I'm here. So that I have all my ST plus ones that I'll have 361 of these things. Um and then

Host (host): to be clear, this is like action one, action two, all the way to action three sixty one. Exactly.

Guest (host): Yeah. And the um we have to estimate the value of each one of these. And so then we have to invoke the model all 361 times to give me values for each one of these things. And then I will select I'll select it based on the the UCB, the upper confidence bound, which is this equation that is roughly something like um balancing uh my value function of S T plus one, which they're gonna they in the literature it'll be called the Q value because it's actually. The difference between a uh value function and a q value is just that I have the action as well. Yep. So it's B S T, then AT. Um So we'll just call that Q value, which is my um exploitation term. And then my exploration term will be something like uh it's this funky square root of n. Uh so it's the argmax of A of my Q. And then I have this, which is the probability of this this move being played, which we have from here of of S, let's just call it S T. Plus one. And then I have this term, which is this sum over uh N S B divided by N S A. And

Host (host): what's what what's the intuition behind this term? So that's

Guest (host): what these N's is is the the visit count during my MCTS process. So this whole tree I'm going to

Host (host): So this tree could get really big, right? It's 361 per thing. So we can't

Guest (host): visit the depth of 30.

Host (host): So you can't visit every single leaf

Guest (host): though. Exactly. And so you wanna keep track of which uh which state did you end up in and what action did you take when you were in that state. And you wanna make sure that you s you have good exploration, right? And so The way you keep track of the way you ensure that you have good exploration is you want to not just be greedy and always pick the highest value one because that could be local very myopic. And so what you'll do is during this MCTS process, you'll start this dictionary, which will be all zeros of the visit count of being in this state and taking this action. Yep. And then once you go through your first rollout. You'll do you'll go here, you'll all these things will be in edit to zero, you'll have some probability. What we're gonna bias it towards the higher probability uh of places to go and then we'll go go we'll expand those trees and then we will um update the counts that we visited this and that will basically reduce the amount of uh uh probability that we're gonna select it again because this this will reduce my my exploration term and if it's highly valued then we're gonna increase the Q on this because this is the expected value of going down this this this path. So the

Host (host): the gist of it is fundamentally like you want to take the optimal ish path But have enough exploration in this really expensive uh step you're doing here, so that you are making sure you're getting a decent chunk of the other potential Leaf nodes you could traverse to in these 30 step rollouts.

Guest (host): And so I'm gonna do this this MCTS simulation eight hundred times here. And then e for all eight hundred, I have to go through this whole process and I have to invoke the model like at least thirty times to get through all here. And so that's You know, 27,000 800

Host (host): times 30.

Guest (host): Yeah. Invocations. Uh 24,000 uh invocations of the model to to develop this tree. And then once I have

Host (host): per step.

Guest (host): Per step. Just to do one action into the game. A lot of people don't understand that this is like you don't like store this MCTS tree. You like you throw it away after uh uh you you make the move. Um, but once it's very expensive to develop this MCTS tree. And once you have it, the probabilities uh of traversal are actually extremely useful for training. And then you end up biasing it and you train it with the MCTS tree, which is like a little bit seems like circular motion or something like that, like uh, but you end up treating that as as the pi that you'll train in your loss function. Um so you we have the R of did we win or lose? We have the the pi of of what was the end result of this whole uh expensive process. Um and then at test time we are going to do these 24,000 steps every single um uh every single move to pick the argmax uh that gives that that s satisfies both exploration x and ex exploration and exploitation.

Host (host): In this case, you know, this still feels somewhat tractable though, because the action space is small enough where this like kind of works. Exactly. Now like let's say hypothetically maybe we can draw like an an imaginary go a game of Go where it's like You know, let's let's let's say this game ago was like a thousand by a thousand. And so now you have A equals uh you know more or less uh a million. And now this this tree uh we're drawing here.

Host: That has to take here. This has cardinal or like you know width, I guess, 1 million. Right. And there's like S0 through S1 million. And the number of uh you know steps you would have to take here, presumably have to be way more than 800 in order to get any reasonable uh kind of sampling of this. And so you're probably multiplying the test time cost. of doing a rollout or of doing a of a next step prediction astronomically. If the game was even, let's say, you know, this is only a hundred X bigger than the current game, or not even fifty X bigger than the current game.

Guest: Everyone was very excited about AlphaGo and a at the time in what was this, twenty seventeen, uh twenty sixteen. Uh everyone's very excited about this. And the important thing to pick up is that we did 800 uh MCTS simulations and to cover 361 possible actions on average. So that gives us about two samples roughly on an expectation for every single action. So here

Host: you need like two million of them for a similar depth. To for it for a similar

Guest: depth. And then that's still to do a depth of 30, I would still have to do this times 30. This would be 60 million uh invocations of the model. So that better be a small model, right? That's a lot. Um so yeah. So

Host: that's to do a single action to be clear.

Guest: Yeah, so exactly to do one action. So just imagine uh so why AlphaGo uh doesn't scale.

Host: Yeah.

Guest: To me, there's one. Uh the cardinality of the action space must be extremely small. If it's big, sad. Yeah. Uh two, the um I need a perfect uh deterministic environment, right? Like this, this this doesn't change. The rules of this game don't change. But like the rules of the stock market change all the time. Yeah. The rules to like venture change all the time. Like the real world changes quite often. So uh like uh homo schedastic. Uh and real time. If you saw the the movie, the documentary is which is just such such an amazing documentary, I'd highly recommend it to anyone that watches it. Um the guy is sitting there for like 60 seconds, maybe five minutes, waiting for the computer to like decide. And and it's kind of like imagine we were driving a car and like you took like 60 seconds to like Turn the steering wheel, everyone's dead. Like the whole car is dead. Right. And so like, you know, uh now let's talk about uh robotics and self-driving car, um and why this why that approach kinda can't scale.

Host: Yeah, I think it's a really good contrast here because intuitively, uh I think in thinking through this exact star layout, it actually really changed how I think about the kind of problem space of both of these two. So like let's take self-driving car as an example. This is one, you know, many people have started to experience for the first time because we have some self-driving cars that actually work. You have Waymo and Tesla FSD and whatnot that seem like they kind of work. So like let's maybe have apply your same star Framing here. Um, I would contend that the state space of self-driving car is enormous. And it's actually not intuitive to me whether it's more or less large than this one, right? I mean, in a sense, the chess in AlphaGo state space is already like more than the number of atoms in the universe or something to that effect. Right. But like just to emphasize that here, you know, you are considering, you know, surroundings, vehicle state. Yep. Uh like, you know, camera like weather. I guess the point is like road conditions it's like massive. This is massive. Correct.

Guest: Yeah. Um and and so is the uh space of pixels. Like you know, like what can I put in an image? I can take a picture of an image of anything. Yes. Um and so we're able to handle it. And the same thing here, where we compress from the board state. When we don't represent the the board state, we compress it with a comnet. So they have some deep some some some deep common net that actually takes this state and converts it into a latent. Right. And that latent compression is sufficient to kind of like do pattern matching, do s do some type of like symmetric symmetric uh uh equivariance kind of things. And same thing with this. And even better with JPA, which we can talk about at the end there, which is like basically taking some type of state space. And doing all of our optimization in the latent space, which stable diffusion did uh that worked extremely well, which reduces our state space dramatically because I'm in some latent high-dimensional space.

Host: So like the like the the key thing there is that, yeah, despite this state space being effectively infinite. We've actually gotten really good at compressing this. Yeah. And we'll talk more about some of the tricks for how we actually do this in practice here, but the TLDR is, you know, where there's like ten years of deep learning work that basically makes us extremely good at compressing that very fast.

Guest: Exactly right. Exactly right.

Host: T seems to have a similar problem as before. Right. In fact, maybe even more extreme. There's like infinity other variables around you. Right.

Guest: In some ways, you'd think that it's this is physics. Newton's laws of motion should apply. If I steer turn the steering wheel like this, if I hit the gas, I should be able to really easily m model this. But what is non-differentiable is that I have if I'm going into a a circle, right? It's like the most the biggest issue that that we fa we faced in when I was doing self driving car is like you're imposing your will onto maybe driving in India, I think is

Host: that you're imposing your

Guest: will onto the environment and like people just kind of adapt naturally. Like if you were doing it's a lot of motion, you were gonna gonna collide. And so that the optimal policy if you were doing strict new Newtonians here would be like don't move because anything you do, you're gonna crash. Yes. But it's not true. Like that then we wouldn't function. Like cars wouldn't go down the road. Um and so you have to model the the environ you have to include other people in the environment and uh understand the embodiment of like how your action will change other people's actions. YC's next batch is now taking applications. Got a startup in you? Apply at [ycombinator.com](http://ycombinator.com) slash apply. It's never too early, and filling out the app will level up your idea. Okay, back to the video. Now let's

Host: talk about the action space. You know, like one way to look at the action space is that

Host: It seems relatively small. Seems like, well, you know, you turn the steering wheel left to right, you hit the brake, you hit the you hit the gas. Doesn't seem that big, but like how big is it actually? Like how do we actually represent these action spaces when it comes to a realistic self-driving car scenario?

Guest: Yeah, I I don't know how they how they do this nowadays. Um they they're doing a whole bunch of like bird's eye view, different things like that. That's

Host: considered even just like a very s simplified.

Guest: But what do you have? You have a steering wheel that you can turn left right, you have uh A brake pad and you have the gas. Yeah. And so I

Host: guess this thing is like 365 degrees. Yeah. So it's like a 1 to 365, let's say. Yep. Or 0 to 365. Yep.

Guest: And you had let's just say you break this up into 10 different uh uh severities. You're

Host: already uh even with just this oversimplified model, your action space cardinality is 365,000. So that's like A hundred X bigger than AlphaGo. It's in fact it's about the size of the example or it's in fact like decent amount smaller than the size we said.

Guest: And so yeah, so thirty six thousand action space is very large. And then even worse, unless you're Tesla, we have a bunch of video of people driving cars. We don't have video of like dash cams and like that. Like You actually don't have um again, only Tesla has this of the action as well. And so the the things that you have access to, that your trajectories are just like S T, S T plus one, yes, S T plus two. So

Host: there's a you're saying there's a decent number of these that's from like dash cam footage on YouTube or something, but not really that many either. Yeah.

Guest: Relative. If you wanted to do a self driving car and you didn't want to go spend a million dollars, trillion dollars on going collecting all this data, then you want to leverage this data somehow. And this we're this is gonna be really applicable for uh robotics because we have a lot of uh uh videos of people doing things. Yeah. Right? Especially with egocentric. Like we we have the those videos, but we d what we don't have is

Host: the actions they take. Yeah. Yeah. So this is like This is this is a sequence of what you're showing here. Unless you're Tesla. Unless you're Tesla. And Tesla has

Guest: this. So this is the a huge competitive mode of like what do people do in that state? And then so you can behave your clone to go from here to here, from here to here, go here to here, etc. But even then, it's still very, very difficult. You have to it's it's not sufficient. People think that like, okay, I have this, we have a self-driving car, right? I mean, the amount of work that they're doing at FSD is like incredible. And it's it's not generally available, like you can't it's you know, it's not Waymo level um yet.

Host: Would this be a good moment to briefly talk about model free versus model-based RL? Yeah. I think that's an important distinction that's going to be relevant when we talk about more world models. Yeah,

Guest: so this is a perfect point. Um so model free just means that my my policy pi uh of a t given st Uh I have no world model involved. It's literally it's literally doing what I said. I grab a bunch of these and I train go from S to A. S to A. Just press

Host: the next day. That's

Guest: it. And that's and this is l logic called VLA. Um you know, this is like giving us pretty good results. It's behavior cloning, it's all the the the the stuff that it's not getting us to Rosie the robot just yet. But uh in

Host: many ways, it's the closest thing that just looks like the next token prediction from LLMs that seems to scale pretty well with natural language. I mean it's It's not exactly the same thing because there's no action exactly, but picking a token is not exactly the same thing, but it's very analogous to that. Like basic thing the same

Guest: thing. I basically take away the the tokenizer head and I give it an action space and I collect a bunch of teleops data, you know, like this, as as the self driving car does in Tesla. And I just take in the the state, which is some image and or maybe sequence of images, and then I'll output some action and that's it. Cool. And this is let's say model three. Because I don't have a model for the environment. And then now if I do model based RL, I have not just some pi, but I have also pie uh psi as well here. And so uh by Uh by including this, I can have a much stronger policy, but it would take a lot more time to perform inference because I have to do this full test time planning.

Host: Just to remind us, that psi is referring to this specific transition function, right? It's referring to this. You're saying this is specifically referring to um a function of S T plus one given S T and action T. Yes.

Guest: So it's

Host: like your ability to predict the next state you'll be in is is the crux of it. Yep. As opposed to just directly predicting

Guest: the actions. Yeah. And the main thing that I believe is that this is required for AGI. This is what the hu the human brain is is

Host: at least in the way the human brain does it.

Guest: Yeah. And let me go further in saying that like if you look at the um Billions of years of evolution. Basically, there's this thing called 10 million 10 million years ago called the great cortical expansion, which you see the size of a brain just explode, get bigger, bigger, bigger, exponentially up until us, and it basically stops. And if the entire point of the neocortex is world modeling, what happened is we started from VLAs. This would be like

Host: Ants or whatever

Guest: and fish. Yeah, right. Just like very like, you know, lizard brain, whatever you want to call it. And then we develop this neocortex to like, you know, go from our our motor cortex to actually simulate what's gonna happen. And that makes us just so much smarter. And then we once we get those samples, we can compress it when we sleep or otherwise. with this hippocampal, shortwave ripple, whatever you want to call it. And then that helps us uh develop a better policy. And that marriage between the two is is not only helps us um train on hallucinated uh examples, but it also allows us to test time plan.

Host: Right. I guess the the kind of extreme case then of self-driving car is

Host: Kind of general robotics. Yes. Right. So if you're if you're like a humanoid company like Figure or Pi or whatever, again, same S T A R setup. Yep. I I guess the gist of it is that A is now even bigger. Yeah. Right. It is like I guess a very simple robot would be, yeah, how would you how would you parameterize the action space? Like let's like let's take a very basic

Guest: one. If I take like my six axis uh arm as your your standard here that we're actually working on right now in Stanford Robotics Center, um you have two degrees of freedom, two degrees of freedom, two degrees of freedom. Uh and then you have another two for the end effector. Right. And so that's a simple end

Host: effector, not even like a not even like a

Guest: one axis like You know, we you can rotate, but you have the the the the one axis Yumi style uh thing. So this is eight. So you have sixteen degrees of freedom. Yeah. And let's just say that you do the three sixty-five to what I 10 or whatever, you know, kind of thing. I mean ten it's like ten

Host: to the sixteenth.

Guest: It's like it's insane. It's like yeah, it's an insane number. Um and so much bigger than self-driving car. Um, and even worse, like getting teleops data is extremely painful and expensive. It's not just like, oh, we'll just get some people in the Philippines, we'll give them like some, you know, things or whatever. It's like totally, totally doesn't work.

Host: And nor is there yet something like uh Tesla's fleet, where there are cars deployed that people are just using and they're not even necessarily realizing that every time they turn the steering wheel, they're providing this this data set for Tesla training. And then

Guest: even worse, you have this like what's called cross-embodiment gap. And so if I were to like train this policy on Tesla model X, and I were to like put it on a Tesla model three, it wouldn't work. No. Like it totally wouldn't work. Like all the so much, so much of this uh the the way that if if i were to break on a model three versus a model x the model x it weighs more it has different dynamics aerodynamics and things like that and so what's actually going to happen is very different like the the degradation you have across crop across embodiments is very very very strong

Host: and clearly Tesla's favorite various ways to get around that i mean they they have these that roll out but actually even with Tesla's new FSD today they don't roll out in all the cars at the same time probably for more or less that reason and the in this case it's even harder now I mean you have Bigger differences between embodiments than a model three versus Y. Yeah. And you have way bigger action spaces. You have to somehow

Guest: model. Yeah. Uh Lane Macintosh, I played hockey with at Stanford, uh uh who now runs Tesla FSD. Um I can ask him, but I would bet money that they shard the data per model, per uh car type. Yeah. Wouldn't be surprised. I th I just cause that's what I would do. Like there's no way that like, you know, I I would trust You know, data that was collected on a Model X on a model three. I just with no way I would trust

Host: it. Okay. So now that we understand the basic setup here and why the action space problem is so big, why don't we talk a little bit about how world models actually fit into this? You know, maybe first, you know, I guess what didn't work about the naive world models and how do we fix those? And then let's kind of talk about some of the newest world modeling techniques. Cool.

Guest: So, like in robotics in particular, it's very hard to get these this kind of trajectories that you want, that you kind of need to train for your VLAs. And people spend up, you know, uh, with a whole bunch of teleops data. It's very expensive, very expensive. Ideally, what we would do is take like data like this from someone who is just like puts a camera on them and just like making sushi. Okay. Like, I want to make a sushi robot. Um, how do I do it? Give it to all the sushi chefs, don't put anything in their hands and just have them start cutting up sushi and making sushi.

Host: And ideally we would train it in that way you were describing of like somehow we would train a model just on these two and then later add this afterwards.

Guest: And so the first real person that um you know went after this was Jurgen Schmidhuber. Uh please uh you know so so he doesn't yell at us, we have to we have to make sure we cite him. Uh But he has this really cool paper called World Models, uh, very aptly named. And it's basically he took these like um open AI gym classic uh games, car racing and I think Doom as well, and then just like trained a model. At that time, it was like an RN. Um, he had some funky uh uh zero order stuff in there or whatever. But basically the key premise was I can take an environment, I can extract a whole bunch of this type of data off of it. I think he actually does actually this data, but we'll get into Dreamer where he does it in this paper in this way. And then uh trains a policy on only the uh the synthetic data, the imaginated uh rollouts, and it actually performs well in the environment. This is the first time, in my understanding, that that actually happened and it actually works really well. And

Host: so the key thing there is you can basically use this If you have some predictive model of this in that case and eventually of this, you can use that as basically a synthetic training set to train your policy model and then basically fine-tune it on real

Guest: data later. Exactly. And which is just like a really powerful idea, especially since in robotics, the limiting step is access to large amounts of state action data. And so now the Dreamer series. So basically this published publishes in May of 2018. Uh Danijar uh Hafner Publishes Dreamer 1, I think, in November of 2018. And then now he's been on this rampage for the last seven years, publishing these papers. And Dreamer V4, I think, is the capstone of it. Um, where he ba basically does the same thing and he focuses on Minecraft. Um, and he trains these the a world a world model on this type of data. And then injects action conditioning on a very small amount of data to get to this type of world model that can that has the action conditioning as well. And then samples a lot from it. And then trains a policy on those synthetic uh imaginated rollouts. And it's the policy is so good that it's the first paper to mine diamonds in Minecraft. I'm not a big Minecraft player, but apparently that's extremely difficult. That's like next level difficulty. And it did it all on synthetic data, which is kind of

Host: crazy. And the key unlock there, yeah. Use synthetic data specifically on a model trained on just this sort of state transition type of thing. Yes. And this ends up being very convenient because it turns out. We as a society have a lot of this.

Guest: Exactly. Yeah. All of YouTube, right? He does do a very small amount of data from ac for to enable the action conditioning. And that get that allows you to do this full uh simulated rollout. But yeah, it's true. So we have we have YouTube, we have like Flickr, we have all these data sets online of like, you know, people doing things. We'd like to use it. And no one has really gotten that to work. And then now that with this um these like video generated generation models, we can take that data, create a world model out of it, add action conditioning, post-train it with action conditioning for some new task that is we want it to do, chopping down wood or uh, you know, um making sushi or folding my bed or whatever it is, only a few amount of examples. And then we can train a policy on this in this neural uh simulation. Yeah.

Host: And you know, we put out a video um about diffusion models fair recently and flow matching. I imagine that now ties very closely to this, right? Ultimately the the kind of current state of the art best way to do this on basically infinity data that we have available and can keep generating is using state of the art video diffusion or slash flow bashing.

Guest: Exactly. Yeah. So like if you have your your C Dance or your Sora or One or One, exactly all those models, like basically the idea is now we have them and they're already trained and they're great. Let's do a small amount amount of action conditioning on them to get to this uh this world model, and then we can sample from it a bunch and then train. And this is exactly what Wave uh did with Gaia. And Gaia, I think they've raised one point five billion dollars to to basically run with this idea for self-driving car. Um I think a bunch of companies, um, NVIDIA uh uh this this paper here, uh uh is basically talking about doing exactly the same this dream zero for robotics um and

Host: what i thought was really cool about this paper is that they yeah they do exactly this process where they have this um joint model of um state transitions and actions They train it by first instantiating it with the open source one video diffusion model. And then it only takes them about 500 hours of teleop data, which is basically exactly this to get it to be pretty good. And they have a lot of clever tricks that allow it to be cross-embodiment and work on unseen tasks with relatively small amounts of data. Right. And and it really is taking basically the exact concept, I believe, from the Dreamer paper and applying it specifically to these robot embodiments. Exactly. And it turns out it actually works uh actually better than I would have anticipated it working.

Guest: So yeah, so I think that this is basically the the the path to it was the path, I believe it was the path to get humans uh uh to be as good as we are genetically over the last 10, 20 million years of evolution. A bigger world model helps uh for training and for uh test time planning. Um and I think it'll be the same thing as true as ro for robotics.

Host: What's also cool is there's a bunch of applications of this to things outside of robotics too. I mean there was a weather planning paper, for example, we were reading this GenCast paper, which I think applies a relatively similar concept um in terms of how they model, you know, literally the world the world's weather um with something

Guest: like this. Yeah, we have to talk about the world model for the world. Um Yeah. So basically they do this exact same thing where you know the key unlocks for this whole thing was getting diffusion to work in very high dimensional state spaces like we talked about in the last uh lecture and then learning to to use that to can action condition in the way that he's done. But they did this for the entire world with this exact same diffusion steps, which go from some and they go back two uh two time steps, lag of of order two, AR two for the statisticians there and then basically predict the next uh state of the world based on the those things with this Langevin diffusion rollouts. My my big assertion is that um it was necessary for the human brain To develop world modeling. I actually just this saw this paper that I wanted to make sure to call out because I thought it was so great. Uh out of uh University of Washington, where they say explicitly in the in the abstract, each cortical area estimates both latent sensory states and actions, and the cortex as a whole predicts the consequences of those actions. That sounds like a world model to me. No. Right. Um

Host: it's actually describing exactly these two equations here. Exactly. Where we're estimating both the sensory latent states and actions. I mean, I guess it's really the joint model that we showed earlier. Right. Is what he's describing here. It's exactly this equation that he's showing

Guest: now. Exactly right. And so uh if it works in us, it should work in robotics. Um and I think that that takes us the rest of the distance.

Host: Why don't we talk briefly about latent world models, especially the con the JEPA concept? Because I think there's been a number of Papers that use JEPA as an element of their architecture. Why don't we just briefly introduce JEPA and how it fits into the current landscape of world modeling?

Guest: Yeah. In classic RL, you'll have like, you know, if you do study Q learning, for example, you basically keep this matrix called the Q matrix. Yep. And it's going to be uh S by A. And so I have this um S, but states and actions, states and actions, and each one I need, you know, some um amount of counts of being in this state action, uh And I take the average value of being of taking that action in this state. Yes. And that's the my Q value there. And it's a little bit more complicated than that. There's Bellman equation, all this backup, all this stuff like that. But so this scales horribly because as the cardinality of my space space gets bigger and my cardinal action space gets bigger, stuff I don't have enough time I I become less and less sample efficient. Right. And so in the

Host: last case in the case of like robots or whatever, state is like, yeah, it's this whole thing we described earlier, right? It's absolutely massive because it has all of these elements in it. You couldn't really enumerate a huge grid.

Guest: And so the classic trick, I mean, since I took, you know, uh C229 with Andrew Ng in 2012, is you do

Host: this. It's like a neural app work on it. Exactly.

Guest (host): And you basically are just going to compress that state into some lower dimensional state space. This actually predates deep learning. Uh we were doing stuff like this. Um, I think my first paper was basically doing something like this. Uh basically turning like a grid into like uh a bunch of like pyramids. And like and and the state was how much I'm in pyramid one or pyramid two or whatever. But anyway, the neural network can just do this. And so basically what uh the the key idea in JPA, if I have um in image one and I have image two and I have image three. I can do my my world modeling, uh my my world modeling of s t plus one uh given st and at in pixel space and have this is uh let's say at time t t plus one. T plus two, et cetera, et cetera. And I have to actually predict now the full uh image. That's extremely expensive from a computation standpoint and also from like a sample efficiency standpoint. What I can do instead is put this through some comnet.

Host (host): Some encoder.

Guest (host): Some encoder. And then I'll get a latent for T. And I'll have a latent for T plus one. And I'll have a latent for Z T plus two. And then I'll have from this, from ZT, I want to predict Z T plus one hat. And my goal is to make this and this uh make and my loss function will be something very simple like Wanna minimize this.

Host (host): That's it.

Guest (host): Now this doesn't work. This collapses hard. And so what happens like is basically just if you out if you just predict zero.

Host (host): Yeah, it works. Yeah.

Guest (host): Just output zeros, which the model will learn to do. Yeah. And I'm actually incorporating this into my current research right now. Um and so what you need to do is something called sig, or uh this is one technique, Vic reg is another, where basically I add this another term that basically says uh I want the um over a large enough batch size, I want the the distribution of Z T plus one to follow a Gaussian, you know.

Host (host): It's kinda like a normalized like a like a batch norm type of Yeah. I mean not in the same

Guest (host): way. If if it's zero, it can't be this. Yeah. Right? Because then this is non-zero. And so maybe I think that there's probably this or something like that. But basically this prevents it from modal collapse. And it makes it do something good. And this is the most recent paper for the audience is LEWM, LE World Model, which is super, super great. Um, however, to be completely frank, the This this is self-supervised learning, super great. It doesn't work that well. If you were to not do uh these techniques, and there's there's a bunch of other techniques that you can do, uh, it will actually outperform much better. And that are, let's say, for example, um, if I'm gonna do an LLM and you have like, you know, Francois uh likes sushi, which is definitely true. Um, and I tokenize this into a bunch of different tokens here. And this is token ID six, nineteen, twenty-eight, whatever, and I look up the encoding into this, and that's gonna be uh E1, E two, E three, etc. Um what you can actually do is have the LLM output uh what the LM will take in take in these things and will output um the the next token. And so it'd be like let's call it H. Uh this would be the logits coming out of it, T plus one. And what you can do is actually have this be close to E T plus

Host (host): one. Mm-hmm.

Guest (host): And a lot of people are playing w with this idea and getting rid of the cross that should be lost entirely. And so if you were to do this. It actually is a proxy for the cross-entropy loss, and there is no cross-entropy loss. And the the cross-entropy head is actually very expensive. Yep. And so this is very cheap. And like this literally just grabbing it. So people are ch playing around with this idea, um, and as a as a basically as a as a cheaper proxy for the cross-entropy loss. So there's a lot of different ideas on basically uh taking this JPA idea to not just pixels, but to L LMs

Host (host): as well. Yeah. Interesting, yeah.

Guest (host): So just to define what JPAI is, it's joint embedding predictive architecture.

Host (host): I I think one of the things I find uh cool about this JPI idea is it feels like an idea we see over and over in deep learning. There's a version of this idea that's basically the staple diffusion idea. Yep. There's a version of this idea that in my company training graph convolutional neural networks to um design drugs we use to do, you know, latent variable generation, for example. And it's like it's like an idea that comes back over and over and then has this, yeah, various tricks that it actually takes to get it to work in practice. Okay, now we have a pretty good sense for how world models work. We have a pretty good sense for what the state of the art looks like. If we trust this paper, and it seems like these kind of work on robots too. I mean this paper's only from the end of uh end of last year and this year, and it seems like they have various methods that allow you to train on relatively small amounts of data that's tractable and pre-train on the diffusion models. So are we good? We're done. Does it all work?

Guest (host): Yeah. This is twenty sixteen. Yeah, no. I don't

Host (host): think so. What are what are one or two, you know, because there's lots of open problems remaining. What are like a few open problems maybe we can emphasize here that the community can go emphasize working on?

Guest (host): Yeah. So um I think the first one is that uh pins doesn't really work. What is pins? Physics informed neural networks. So pins. uh doesn't really work. This is physics informed neural networks. And so basically if like almost all of the self driving car data looks like this, but the car is driving down the road. And let's just say, for example, uh I have, you know, uh a house here. And I want to train the model on you know not driving into the house. And so let's say I put I put it into a state right here to drive into the house. What's gonna happen is because almost all the data is like looks like this driving down the road, this will just turn magically into like a highway. No. And I'm just like, boo, it just don't worry, it may crash

Host (host): off. It basically needs like a ton of data not to do that either from simulation for that to not happen.

Guest (host): In fact, I actually don't even know if because of the data distribution, there's no data here. There's almost all the data here. And like when you're training a neural network, it has a a tendency to collapse if you don't keep the mini mini batch composition uh like very even over the, you know.

Guest (host): uh uh over the class space or whatever you want wanna want to call it but like you'd have to train on uh you have you have to be very careful about your data mixing to make sure you get this right to solve this problem that no one really has. But even then the if you take just a simple thing like this, this is like the the the conic example and I have a some sine wave and I want and I have these as my X And I have these as my Y. So this is complete interpolation. No. Uh maybe mess this up. But why?

Host (host): Like this. No.

Guest (host): We can't get to like machine precision. We can't. What is it? I don't know. What is it 180 minus 16 or whatever it is? We can't, we we the SGD will not get to zero effectively zero. So we'll always have some residual. And for us to be like a really good world model to simulate body interactions, like to to simulate this, what's gonna happen when I do this? And like let's say that I'm trying to be LeBron James. Yeah. Like there's like I saw this one video of um Steph Curry dribbling about uh basketball on a court and he just felt that there was a dead spot in the court. And he because he's so good and he knows exactly the physics of what's gonna happen. If I hit this, you know, the ball with this force, like the ball is gonna come back exactly this spot, and it just didn't. And he knew it wasn't him, it was the the court. And he found a dead spot in the court. Like that's how good the the the human brain is at world modeling. In my opinion, I think it's an SGD issue. I think it's probably an architecture issue. I think Sam Altman just kind of came and just said that he thinks that there's definitely an architecture that's gonna be more performant than the transformer. I think he's right. Um I think the the the transformer doesn't do compression uh uh in the time domain at all. It just keeps around everything. Um so anyway, so I think that the getting higher fidelity. in the world model is extremely important. One. I think two. It seems

Host (host): like test time probably is gonna be big thing, like adaptation. Exactly.

Guest (host): Test time planning. We the how quickly the human brain can, you know, it in times of in sports and things like that, when you're playing tennis, I think you're a tennis player, like how quickly we can it adapt to what a player is doing and things like that. We're not going to sleep and like retraining. We're we're very quick to adapt to a new new environment. It's like

Host (host): the out of distribution prediction. Exactly. It's really challenging. And like

Guest (host): one little data point we can like quickly adapt to that new thing and change. Um, I think there's been a lot of papers uh uh on like basically estimating the the the friction coefficients. And so like those can change over time if you go to a human environment or not, for example, like this this friction might change and that's important in control. No. Um and so you need to estimate that very quickly and adapt. And the these models just kind of don't have a mechanism to do it.

Host (host): Yeah. And then I guess there's like the practical s speed elements of these, right? A lot of these are doing some sort of expensive planning step. Mm-hmm. And we're doing some sort of like uh we're we're kind of hacking around it with this pre-training process and synthetic data. But even so, like to really get maximum performance right now, you'd want to do something that's closer to like the AlphaGo style rollout, and that's extremely slow.

Guest (host): Right. The MCTS process, which can't happen. Um, the other thing that that is pretty crazy about the way that the brain works is that like everything is kind of running autonomously. And so like you'll you might be like in the middle of saying sentence one and then be like, oh, actually, no, something else. And so, like, what does happen there? It's like type one and type two thinking are happening at the same time in some way. And so, like, there's definitely uh, you know, some. um really cool mix of these like heterogeneous models and like some are overriding others and like taking control of the motor cortex and like commanding the body to do a thing.

Host (host): You know? Okay, but on the flip side now, we um talked in the past video about the squint test and how we felt that auto regressive LLMs maybe don't pass the squint test. Why don't we reintroduce what the squint test was for a second? And then maybe let's think about whether this passes the squint test, despite all those limitations. Yeah.

Guest (host): And the swim test for me, I think, is like, um, this comes from the Yann LeCun. Uh we didn't need uh flapping wings to achieve flight. Um and to that I say, Well, we did need two wings. And like if I squint and I look at a bird and I squint and I look at a plane, I'm like, Yeah.

Host (host): It's kinda similar. It looks right. Yeah.

Guest (host): Um similarly, if I squint and I look at the human brain and I squint and I look at all these these world models, we have like this VLA, this action policy, and that they're doing test time planning together and things like that, it's getting really close. It's much, much closer.

Host (host): Seems closer than an autoaggressive LLM. And that's like this concept of a world model of you know implicitly predicting future states and actions feels intuitively like what our brain's doing. And it seems like there's some, you know, neuroscience evidence to support

Guest (host): that. I mean I'm I'm getting to the conclusion that I think that the brain is the optimizer, not the model. And that the the brain emits like has models that it invokes, but the brain is somehow also the optimizer itself. And so in that way it doesn't pass the squint. Um, because like, you know, something magical is happening when you're sleeping. There's no intelligent species that we're aware of that have any amount of intelligence that don't sleep. And so like octopuses, dolphins, all this other stuff, elephants, they all sleep. There's some reason for that. And that seems like a really thing about like the evolutionary re like. recourse of sleeping. Like you get eaten when you sleep. So like for the benefit of sleeping should be so so much better to outperform that. So I think we don't have this idea of awake sleep uh in our current um architecture. But I can imagine I'm like simulating, you know, you know compress from the hippocampus some like experience in the day. I'm like training on more of those examples, right?

Host (host): You're like collecting a whole bunch of these experience rollouts and then you're updating your your policy function over there. Like like there's this thing called

Guest: shortwave ripple where like the hippocampus when you're sleeping like emits these uh uh spike trains that are actually reversed from when they actually happen back in through the both both the hemispheres and for like seven times and then it like stops. So like there's something happening there that's very uh uh training something. Yeah. And if you don't sleep, then you don't up you don't have long-term memory. Right. Right. And so like there's definitely a reason why we're we're training uh things that happened uh into our brain.

Host: So where does that put us now? We have all this work happening with world models. How should we think about what's coming ahead in these next few years in the research community.

Guest: Yeah, I think that like we're gonna see a lot more uh of these world models in robotic policies. I think that's going to unlock probably full self-driving would be like a uh one of those examples if they can get the real time ness of it. Sounds like that's coming. They can probably solve it with more compute to like have parallel things. And you probably don't need it for like most standard things, maybe like, you know, getting out of we weird parking jams and like things like that would take us some time. similar to the Rosie the Robot, which we've always wanted to have of Rosie the Robot to like, you know, clean up my room for me. Um, I think that like this feels like we're getting to good enough that we can pay up for data and compute to get to Rosie the Robot. It does feel like that. It'll be expensive to collect the data and do the dreamer sequence of going from state to state And then d getting the action conditioning to work. But like I feel like it should

Host: work. Yeah. I mean what's pretty cool is but we see a lot of companies at YC working at every step of this, from the collecting egocentric data, collecting uh the teleop data, training their own world models and action models, um building new embodiments and then making ways of adapting those embodiments. And it feels like this is the first year where you see demos where you're like, okay, this actually like kind of is starting to look like it's going somewhere. Yeah. And it seems like a very exciting year. Yeah.

Guest: So anyway, I think that there are real AI problems to solve still. We talked about pins, we talked about the real time issues. And then on the robotic side, there's real issue. Like it's amazing how effective our epidermis is in terms of we we can detect

Host: detect tactile Oh epidermis.

Guest: And it's everywhere. Yeah. And so like versus, you know, like the We get like one little sensor that only does tactile. We don't have the the friction component. We don't have temperature. We don't have all these the feeling. We can't estimate coefficient of friction very quickly. I can touch something and say, oh, this is smooth. This is rough. It doesn't, we don't have any of that. And if I numb your hands, I actually had this experience uh um uh just recently. If I numb your hands, like you actually can't tie your shoes. Yeah. So you can't perform control. And so, like, yeah, if you like, you know, uh uh If you train enough um on enough human data tying your laces, do I think you can do it with no feedback? Maybe. Maybe. But like how much would you need if you did actually have the human like touch? Like I think it'd be so much easier. Yeah.

Host: Well, there's a lot of more research to do then. Yeah, yeah. Francois, thanks so much for joining us. Thanks so much for watching, everyone. We'll be back for the next episode of Decoded.