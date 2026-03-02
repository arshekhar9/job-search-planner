"""Job search service — curated product roles at top AI companies."""
from typing import List, Dict

# Ordered: Google DeepMind → Anthropic → OpenAI
PRODUCT_JOBS = [
    # ── Google DeepMind ──────────────────────────────────────────────────────
    {
        "company": "Google DeepMind",
        "company_key": "google_deepmind",
        "role": "Product Manager, Gemini Models",
        "location": "London / Mountain View",
        "type": "Full-time",
        "url": "https://deepmind.google/about/careers/"
    },
    {
        "company": "Google DeepMind",
        "company_key": "google_deepmind",
        "role": "Senior Product Manager, AI Research",
        "location": "London",
        "type": "Full-time",
        "url": "https://deepmind.google/about/careers/"
    },
    {
        "company": "Google DeepMind",
        "company_key": "google_deepmind",
        "role": "Product Lead, Responsible AI",
        "location": "Mountain View",
        "type": "Full-time",
        "url": "https://deepmind.google/about/careers/"
    },
    # ── Anthropic ────────────────────────────────────────────────────────────
    {
        "company": "Anthropic",
        "company_key": "anthropic",
        "role": "Product Manager, Claude.ai",
        "location": "San Francisco",
        "type": "Full-time",
        "url": "https://www.anthropic.com/careers#open-roles"
    },
    {
        "company": "Anthropic",
        "company_key": "anthropic",
        "role": "Senior Product Manager, API Platform",
        "location": "San Francisco / Remote",
        "type": "Full-time",
        "url": "https://www.anthropic.com/careers#open-roles"
    },
    {
        "company": "Anthropic",
        "company_key": "anthropic",
        "role": "Product Lead, Enterprise",
        "location": "San Francisco",
        "type": "Full-time",
        "url": "https://www.anthropic.com/careers#open-roles"
    },
    # ── OpenAI ───────────────────────────────────────────────────────────────
    {
        "company": "OpenAI",
        "company_key": "openai",
        "role": "Product Manager, ChatGPT",
        "location": "San Francisco",
        "type": "Full-time",
        "url": "https://openai.com/careers"
    },
    {
        "company": "OpenAI",
        "company_key": "openai",
        "role": "Senior Product Manager, API",
        "location": "San Francisco / Remote",
        "type": "Full-time",
        "url": "https://openai.com/careers"
    },
    {
        "company": "OpenAI",
        "company_key": "openai",
        "role": "Product Lead, Safety",
        "location": "San Francisco",
        "type": "Full-time",
        "url": "https://openai.com/careers"
    },
]

COLD_OUTREACH_TEMPLATES = {
    "google_deepmind": {
        "linkedin": (
            "Hi [Name], I came across your work on [specific project/paper] at Google DeepMind — "
            "the approach to [specific detail] really stood out to me. I'm currently exploring "
            "PM roles in AI and would love to hear your perspective on what makes someone thrive "
            "in the team's culture. Would you be open to a 15-minute chat?"
        ),
        "email": (
            "Subject: Fellow AI product enthusiast — quick question about DeepMind\n\n"
            "Hi [Name],\n\n"
            "I've been following DeepMind's work on [Gemini / AlphaFold / specific area] and was "
            "particularly impressed by [specific detail]. It directly connects to my background in "
            "[your relevant experience].\n\n"
            "I'm exploring senior PM opportunities in AI and would love your take on how the team "
            "thinks about product strategy. Could we find 15 minutes sometime this week or next?\n\n"
            "Best,\n[Your name]"
        ),
        "tips": [
            "Reference a specific DeepMind research paper or model by name.",
            "Mention Google's mission — organise the world's information — and how DeepMind advances it.",
            "Show familiarity with Gemini's product surface, not just the research.",
            "Connect your experience to responsible AI — it's central to their culture.",
        ]
    },
    "anthropic": {
        "linkedin": (
            "Hi [Name], I've been closely following Anthropic's Constitutional AI research and your "
            "work on Claude's [specific capability]. I'm a PM with experience in [relevant area] "
            "and I'm deeply interested in how you balance capability and safety at the product level. "
            "Would you be open to a 15-minute conversation?"
        ),
        "email": (
            "Subject: Product + AI Safety — exploring opportunities at Anthropic\n\n"
            "Hi [Name],\n\n"
            "I've been reading Anthropic's research on Constitutional AI and was struck by [specific "
            "aspect of their approach]. As a PM who has worked on [your relevant experience], I see "
            "a direct connection to the challenges your team is navigating.\n\n"
            "I'm actively exploring PM roles at Anthropic and would love 15 minutes to learn how "
            "the team thinks about the intersection of product velocity and safety.\n\n"
            "Best,\n[Your name]"
        ),
        "tips": [
            "Anthropic cares deeply about safety — show genuine understanding, not just a buzzword.",
            "Reference the Claude model card or a specific policy post from their blog.",
            "Highlight any experience with trust, safety, or responsible AI explicitly.",
            "Mention Claude.ai and the API platform separately — they have distinct user bases.",
        ]
    },
    "openai": {
        "linkedin": (
            "Hi [Name], I've been paying close attention to how ChatGPT's product surface has evolved "
            "— especially [specific recent feature]. I'm a PM with a background in [your area] and "
            "I'm exploring roles at OpenAI. Would love to hear your perspective on the team's roadmap "
            "thinking. Open to a 15-minute call?"
        ),
        "email": (
            "Subject: PM background in [area] — keen to chat about OpenAI\n\n"
            "Hi [Name],\n\n"
            "I've been closely following OpenAI's product releases, particularly [specific feature "
            "or announcement]. My background in [relevant experience] maps well to the challenges "
            "of scaling AI products responsibly and quickly.\n\n"
            "I'm actively exploring senior PM roles at OpenAI and would value 15 minutes of your "
            "time to understand what the team's biggest product priorities look like right now.\n\n"
            "Thanks,\n[Your name]"
        ),
        "tips": [
            "Know the difference between ChatGPT, the API, and OpenAI's enterprise offering.",
            "Mention a specific capability you'd push further — not just 'AI is exciting'.",
            "Acknowledge the pace — OpenAI ships fast; show you've worked in high-velocity envs.",
            "GPT-4o, Sora, operator features — show product-level awareness, not just model-level.",
        ]
    }
}


def get_all_jobs() -> List[Dict]:
    """Return all curated product job listings."""
    return PRODUCT_JOBS


def get_outreach_template(company_key: str) -> Dict:
    """Return cold outreach templates for a given company."""
    return COLD_OUTREACH_TEMPLATES.get(company_key, {})
