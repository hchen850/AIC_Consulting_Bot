"""
Response Templates for Ciocca / BEACH chatbot.
Used to keep replies consistent, short, and professional.
"""

TEMPLATES = {
    "scope": (
        "📋 **Scope / What BEACH Can Help With**\n\n"
        "{answer}\n\n"
        "💡 *Remember: BEACH provides information and resources only — "
        "not formal legal or business advice.*"
    ),
    "intake": (
        "📝 **Application / Process**\n\n"
        "{answer}\n\n"
        "🔗 Apply at: https://www.scu.edu/cioccacenter/students/beach/"
    ),
    "eligibility": (
        "✅ **Eligibility**\n\n"
        "{answer}"
    ),
    "resources": (
        "📚 **Resources**\n\n"
        "{answer}\n\n"
        "🌐 More at: https://www.scu.edu/cioccacenter/"
    ),
    "contact": (
        "📞 **Contact & Timeline**\n\n"
        "{answer}\n\n"
        "📧 Contact: https://www.scu.edu/cioccacenter/contact-us/"
    ),
    "privacy": (
        "🔒 **Privacy / Confidentiality**\n\n"
        "{answer}"
    ),
    "programs": (
        "🚀 **Ciocca Center Programs**\n\n"
        "{answer}\n\n"
        "🌐 Explore all programs: https://www.scu.edu/cioccacenter/"
    ),
    "fallback": (
        "I wasn't able to find a confirmed answer to that in my Ciocca/BEACH "
        "knowledge base.\n\n"
        "For accurate, up-to-date information please:\n"
        "• Visit: https://www.scu.edu/cioccacenter/students/beach/\n"
        "• Contact the Ciocca Center: https://www.scu.edu/cioccacenter/contact-us/\n"
        "• Join the email list for updates on sessions and deadlines."
    ),
}


def apply_template(category: str, answer: str) -> str:
    """Wrap an answer in the appropriate template."""
    template = TEMPLATES.get(category, TEMPLATES["fallback"])
    if "{answer}" in template:
        return template.format(answer=answer)
    return template
