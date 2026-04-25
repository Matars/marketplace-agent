# Hermes bootstrap prompt for marketplace-agent

Use this short prompt when you want Hermes to install/configure marketplace-agent from a natural-language goal.

```text
Set up marketplace-agent for me.

My goal:
<describe what I want to find or sell>

Default vendors:
Amazon and eBay.

Do this:
1. Clone or update https://github.com/Matars/marketplace-agent at ~/fafo/marketplace-agent.
2. Read ~/fafo/marketplace-agent/prompts/hermes-installation-guide.md first.
3. Follow that guide exactly.
4. Create or update my user workspace at ~/my-marketplace.
5. Do not configure demo vendors. Use real providers only: amazon and ebay by default.
6. If a provider plugin is missing or broken, use the repo vendor-builder skill and browser/browser-harness tools to implement or repair it.
7. Run validation and the find/sell workflow from the guide.
8. Summarize what worked, what failed, and the exact next step.

Safety:
- Do not auto-post sell listings.
- Do not message sellers or buyers.
- Do not bypass login/captcha/anti-bot protections without asking me first.
- Keep my personal workspace separate from the engine repo.
```
