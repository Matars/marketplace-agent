# Hermes bootstrap prompt for marketplace-agent

Use this short prompt when you want Hermes to install/configure marketplace-agent through onboarding.

```text
Set up marketplace-agent for me.

Do this:
1. Clone or update https://github.com/Matars/marketplace-agent with submodules enabled.
2. Read prompts/hermes-installation-guide.md first.
3. Follow that guide exactly.
4. Start onboarding by asking me the required setup questions from the guide.
5. After I answer, create or update a separate user workspace outside the engine repo.
6. Configure marketplace-agent from my answers.
7. Use the bundled browser-harness submodule at third_party/browser-harness for vendor discovery/scraper repair.
8. If a provider plugin is missing or broken, use the repo vendor-builder and browser-harness skills to implement or repair it.
9. Run validation and the requested workflow from the guide.
10. Summarize what worked, what failed, and the exact next step.

Safety:
- Do not auto-post sell listings.
- Do not message sellers or buyers.
- Do not bypass login/captcha/anti-bot protections without asking me first.
- Keep my personal workspace separate from the engine repo.
```
