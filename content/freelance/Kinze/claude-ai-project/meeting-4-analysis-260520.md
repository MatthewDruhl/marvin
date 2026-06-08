# Meeting Analysis: North Liberty Software Team - May 20, 2026

## Meeting Arc

The meeting started cautious. Michael asked for introductions and wanted Matt to explain how he got connected to Kinze. Matt was careful to set the tone: "judgment free," "just asking questions," "not saying you're doing it wrong." He was reading the room.

The team was feeling Matt out during the intros. Everyone listed their Intermec pedigree like credentials. 11 years, 16 years, 10 years. They were establishing that they're not amateurs. The subtext was: "we know what we're doing, so what are you going to tell us?"

Matt earned credibility with the Pearson story and the DND project. The DND stuff in particular loosened the room up. You could hear people lean in when he talked about 500 tests and managing PRs. That's when they stopped evaluating him and started talking to him as a peer.

The middle section was the most productive. Jason opened up about their full CI/CD process, and once he did, everyone followed. The token discussion got animated. Gary, Jason, and Matt were going back and forth genuinely working through how to measure AI value. Nobody had a clean answer, and that honesty made it feel collaborative rather than consultative.

Matt H.'s question about shared context was the spark moment. You could feel the energy shift. Multiple people jumped in. Jason said "I would want that." Jordan chimed in. Ryan connected it to their row cleaner domain knowledge problem. That was the moment the meeting went from "here's what we do" to "here's what we want."

The last third got looser. Gemini rants, Emily Druhl vs. Amelia Druhl, chipmunk-speed Alexa. The group was comfortable. That's a good sign. People don't joke around with a consultant they don't trust.

It ended flat, though. Not in a bad way. Jason essentially said "we don't have a lot of pain points" and Matt agreed. There wasn't a strong closing or next step. The meeting just kind of wound down naturally.

Overall arc: guarded start, peer-level middle, genuine excitement around the knowledge base idea, casual wind-down. They like Matt. They respect his experience. They're just not in a hurry.

## Hidden Insights

**Jason is the gatekeeper, and he's skeptical in the right way.** He controls the process, the token budget, the tools. He's not anti-AI. He's anti-waste. Every time Gary or Matt suggested something, Jason's response was some version of "we could, but what's the token cost vs. the value?" That's the person you need to win over with concrete ROI, not enthusiasm. If Jason adopts something, the whole team follows.

**Matt H. is the untapped one.** He's on the embedded team, hasn't dived into AI yet, but he's asking the most forward-looking questions: shared context across developers, SSO unification, "why did Jordan make that change?" He's thinking about team-scale problems, not individual productivity. He might be the internal champion for the knowledge base work if Jason's too busy.

**There's tension between Williamsburg and North Liberty.** Gary didn't know what the NL team was actually doing with AI. He assumed they were using AI for code reviews (they're not). Jason corrected him carefully: "the words mattered. Code review is the final peer review." The teams are operating independently with no shared visibility. Gary's AI council role is supposed to bridge this, but he's been in the role less than a week ("I've had a good 4 days to work on this stuff").

**The "we built this from nothing" identity is strong.** Jason and the team said it multiple times. No inherited code, no inherited processes. They're proud of it, and rightfully so. But it also means they'll resist external tools or processes that feel imposed. Anything recommended needs to feel like it extends what they built, not replaces it.

**Jordan's 15X token burn is a canary.** He tried the higher multiplier, burned through it in 2 days, and said "a token doesn't really mean anything to me." That's not irresponsibility. That's a pricing/visibility problem. They can't make good decisions about when to use Opus vs. Sonnet if they can't see the cost until it's gone.

**The accounting person's instinct was right.** She refused to put financial data into the chat because she didn't trust it. Everyone in the room treated this as a beginner mistake to fix with education. But her instinct about data privacy was correct. The real solution isn't "teach her it's safe." It's building the infrastructure (scrubbed data, local models, or enterprise agreements) that actually makes it safe.

**Nobody asked about testing.** 2000 automated tests, and not one person brought up using AI to generate test cases, improve coverage, or analyze test failures. For a team that hates inefficiency, that's a blind spot. Their test infrastructure is mature enough that AI-generated tests could slot right into the existing pipeline.
