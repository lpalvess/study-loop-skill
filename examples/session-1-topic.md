# Session 1: topic named in one sentence (English)

- Tool: Claude Code (headless, `claude -p`)
- Model: claude-sonnet-5-5
- Date: 2026-10-09
- Followed the skill's rules: partly. The skill triggered (it checked for saved topics, then started a new study), did not teach the topic, and quoted the learner's own words ("the DNS server knows the address of every website"). It stayed on one gap. But it ended with two questions in one message (what problems would one server run into, and where does the DNS server get an address it does not know), and the scenario it painted leans toward the answer. The brief and SKILL.md ask for one question and no answer.
- Note: the first attempt failed with `Error: Input must be provided either through stdin or as a prompt argument when using --print`, because `--allowedTools "Bash(python3 *)"` consumed the prompt as a second value. The run below used `--allowedTools="Bash(python3 *)"` instead. Nothing else changed.

## Prompt

Use the teach-back skill. I want to study how DNS works. My explanation: when you type a website name, your computer asks a DNS server, and the DNS server knows the address of every website, so it just sends it back.

## Reply

You have no saved topics, so there's nothing to review yet. We'll start with new material.

You got the core right. Typing a name makes your computer ask a DNS server, and the answer is an IP address that comes back to it.

One spot in your explanation is a false claim. You said "the DNS server knows the address of every website."

Picture a single server holding the address of every website in the world. Millions of sites are added, moved or deleted every day, and the owners of each one control its address. Given that, what problems would that one server run into? And if your computer's DNS server doesn't already know an address, where do you think it gets it?
