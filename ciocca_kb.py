"""
Ciocca Center / BEACH Knowledge Base
Source: https://www.scu.edu/cioccacenter/
Last updated: 2026-02-22

Each chunk has: id, title, source, category, tags, content
Categories: scope, intake, eligibility, resources, contact, privacy, programs
"""

KNOWLEDGE_BASE = [
    # ── SCOPE ──────────────────────────────────────────────────────────────
    {
        "id": "scope-001",
        "title": "What is BEACH?",
        "source": "https://www.scu.edu/cioccacenter/students/beach/",
        "category": "scope",
        "tags": ["beach", "overview", "what is", "definition"],
        "content": (
            "BEACH stands for Bronco Entrepreneurs' Applied Collaboration Hub. "
            "It is a free advisory service run by Santa Clara University's "
            "Ciocca Center for Innovation and Entrepreneurship. BEACH provides "
            "startups and small businesses with no-cost legal and business "
            "information and resources. SCU law and business students work in "
            "cross-functional teams to research and advise clients on legal or "
            "business concerns. Clients receive free information backed by "
            "research, review of findings, valuable recommendations, and "
            "additional resources."
        ),
    },
    {
        "id": "scope-002",
        "title": "What is the Ciocca Center?",
        "source": "https://www.scu.edu/cioccacenter/",
        "category": "scope",
        "tags": ["ciocca", "center", "overview", "mission"],
        "content": (
            "The Ciocca Center for Innovation and Entrepreneurship at Santa Clara "
            "University helps prepare students for entrepreneurial leadership through "
            "a variety of opportunities within diverse organizational settings. It "
            "provides networking, educational, and advisory services. The center "
            "supports the professional development of university faculty and staff "
            "in the areas of innovation and entrepreneurship. Programs include "
            "BEACH, Bronco Ventures Accelerator, Business Pitch Competition, "
            "Venture Capital Competition, Mindset Scholars, Innovation Fellows, "
            "and more."
        ),
    },
    {
        "id": "scope-003",
        "title": "What BEACH is NOT — Limitations",
        "source": "https://www.scu.edu/cioccacenter/students/beach/businesses/",
        "category": "scope",
        "tags": ["limitations", "not legal advice", "not business advice", "scope"],
        "content": (
            "BEACH is NOT a formal engagement — either as legal counsel or as "
            "formal business advising. BEACH provides information and resources "
            "only, not official legal advice or formal business consulting. "
            "BEACH students are not acting as attorneys or certified business "
            "advisors. Clients should not rely on BEACH outputs as a substitute "
            "for professional legal or financial advice. BEACH cannot represent "
            "clients in legal proceedings or make binding business decisions "
            "on their behalf."
        ),
    },
    {
        "id": "scope-004",
        "title": "Types of questions BEACH can help with",
        "source": "https://www.scu.edu/cioccacenter/students/beach/",
        "category": "scope",
        "tags": ["topics", "help", "legal", "business", "startup", "small business"],
        "content": (
            "BEACH can help with: business formation questions (LLC, corporation, "
            "sole proprietor), intellectual property basics (trademarks, patents, "
            "copyright), contracts and agreements overview, employment law basics, "
            "marketing and business strategy information, funding and investor "
            "readiness resources, regulatory compliance overview, business model "
            "review, competitive analysis guidance, and referrals to additional "
            "resources. The service is geared toward startups and small businesses "
            "at any stage of development."
        ),
    },

    # ── ELIGIBILITY ─────────────────────────────────────────────────────────
    {
        "id": "eligibility-001",
        "title": "Who can be a BEACH Client?",
        "source": "https://www.scu.edu/cioccacenter/students/beach/businesses/",
        "category": "eligibility",
        "tags": ["client", "who can apply", "eligibility", "startup", "small business"],
        "content": (
            "BEACH clients are small businesses and startups that would like "
            "business and legal information and resources. Clients can be at "
            "any stage of development — from idea stage to established small "
            "businesses. Many BEACH clients come from other SCU programs such "
            "as the Bronco Ventures Accelerator or My Own Business Institute, "
            "or from external organizations such as SCORE or the Small Business "
            "Administration. Clients are primarily recruited from the Silicon "
            "Valley startup community. BEACH serves up to approximately 80 "
            "clients per year."
        ),
    },
    {
        "id": "eligibility-002",
        "title": "Who can be a BEACH Student?",
        "source": "https://www.scu.edu/cioccacenter/students/beach/",
        "category": "eligibility",
        "tags": ["student", "volunteer", "eligibility", "apply"],
        "content": (
            "BEACH students are SCU student volunteers who provide information "
            "and resources to BEACH clients. BEACH looks for motivated, curious, "
            "and enthusiastic students ready to contribute value collaboratively. "
            "Teams consist of law and business students working together. "
            "Students first apply to the BEACH program and are then organized "
            "into cross-disciplinary teams. The program includes approximately "
            "10 groups each session, each with two law and two business students, "
            "supported by experienced mentors."
        ),
    },
    {
        "id": "eligibility-003",
        "title": "Who can be a BEACH Mentor?",
        "source": "https://www.scu.edu/cioccacenter/students/beach/become-a-mentor/",
        "category": "eligibility",
        "tags": ["mentor", "eligibility", "professional", "advisor"],
        "content": (
            "BEACH mentors are experienced professionals interested in consulting "
            "or advising. Mentors guide cross-disciplinary student teams and "
            "work with small business/startup clients through client discovery "
            "meetings, research, analysis, and final presentations. Mentors "
            "understand the importance of the entrepreneurial mindset and the "
            "value of collaboration and teamwork. The expectation is to recommend "
            "practical, student-driven next steps that lead to ideal client "
            "solutions. Mentors apply via the BEACH Mentor Application form."
        ),
    },

    # ── INTAKE PROCESS ──────────────────────────────────────────────────────
    {
        "id": "intake-001",
        "title": "How to apply as a BEACH Client",
        "source": "https://www.scu.edu/cioccacenter/students/beach/businesses/",
        "category": "intake",
        "tags": ["apply", "client", "how to", "application", "process"],
        "content": (
            "To apply as a BEACH client: (1) Complete the BEACH Client Application "
            "form at the link on the BEACH page (https://share.hsforms.com/1mVfaWY8wSq6huE9FkON6AAcbc5l). "
            "(2) As a client, you must commit to being available and flexible for "
            "both the Discovery Meeting and the Advising Meetings to ensure students "
            "have a valuable learning experience. (3) BEACH is offered at no charge "
            "to clients. Applications open each BEACH session — check the Ciocca "
            "Center website for current session openings."
        ),
    },
    {
        "id": "intake-002",
        "title": "BEACH Session Structure and Process",
        "source": "https://www.scu.edu/cioccacenter/students/beach/",
        "category": "intake",
        "tags": ["session", "process", "meetings", "timeline", "how it works"],
        "content": (
            "Each BEACH session involves: (1) Discovery Meeting — the student team "
            "meets with the client to understand their business challenge. (2) "
            "Research Phase — students research the legal and/or business concern. "
            "(3) Advising Meeting — students present findings, recommendations, "
            "and additional resources to the client. Each team of 4 students "
            "(2 law + 2 business) takes on up to 4 clients per session. "
            "Teams are mentored by experienced industry professionals throughout "
            "the process. The entire session runs over a defined academic period."
        ),
    },
    {
        "id": "intake-003",
        "title": "How to apply as a BEACH Student",
        "source": "https://www.scu.edu/cioccacenter/students/beach/",
        "category": "intake",
        "tags": ["apply", "student", "how to", "application"],
        "content": (
            "SCU students interested in joining BEACH as advisors apply via "
            "the BEACH Student Application form "
            "(https://share.hsforms.com/1yUrWjxkiTM26VnwYa84HzAcbc5l). "
            "Students are organized into cross-disciplinary teams after acceptance. "
            "Check the Ciocca Center website and email list for application "
            "deadlines and upcoming cohort openings."
        ),
    },

    # ── RESOURCES ──────────────────────────────────────────────────────────
    {
        "id": "resources-001",
        "title": "Ciocca Center Programs Overview",
        "source": "https://www.scu.edu/cioccacenter/",
        "category": "resources",
        "tags": ["programs", "resources", "bronco ventures", "accelerator", "pitch"],
        "content": (
            "The Ciocca Center offers these programs: "
            "BEACH (Bronco Entrepreneurs' Applied Collaboration Hub) — free legal/business advising; "
            "Bronco Ventures Accelerator — supports entrepreneurial journey from ideation to launch; "
            "Accelerator Prep School — preparation for the accelerator; "
            "Idea Lab — early-stage idea development; "
            "Business Pitch Competition — pitch your venture for feedback and prizes; "
            "Venture Capital Competition — learn VC investment process; "
            "Mindset Scholars — undergraduate scholars program; "
            "Innovation Fellows — undergraduate fellows program; "
            "Venture Virtuoso — entrepreneurship recognition program. "
            "All programs are open to the SCU community including students, faculty, staff, and alumni."
        ),
    },
    {
        "id": "resources-002",
        "title": "External Resources for Small Businesses",
        "source": "https://www.scu.edu/cioccacenter/students/beach/businesses/",
        "category": "resources",
        "tags": ["external", "resources", "SCORE", "SBA", "small business"],
        "content": (
            "BEACH often refers clients to external resources including: "
            "SCORE (score.org) — national retired-executive advisory service offering "
            "free mentoring to small businesses; "
            "SBA (Small Business Administration, sba.gov) — federal resources for "
            "small businesses including loans, training, and contracting; "
            "My Own Business Institute (MOBI) — free online business courses; "
            "Silicon Valley SCORE chapter for local mentorship. "
            "BEACH clients may also be referred to SCU Law School resources "
            "and the Leavey School of Business for additional academic support."
        ),
    },
    {
        "id": "resources-003",
        "title": "Bronco Ventures Accelerator",
        "source": "https://www.scu.edu/cioccacenter/bronco-ventures/bronco-venture-accelerator/",
        "category": "resources",
        "tags": ["accelerator", "bronco ventures", "startup", "launch"],
        "content": (
            "The Bronco Ventures Accelerator is a signature Ciocca Center program "
            "supporting the entrepreneurial journey from ideation to launch. It is "
            "open to the Santa Clara University community including students, faculty, "
            "staff, and alumni. Whether you are interested in starting your own venture, "
            "want to meet like-minded peers, or simply have a business idea, the "
            "programs provide resources and expertise for next steps. The accelerator "
            "includes Demo Day, where ventures pitch to investors and the community."
        ),
    },

    # ── CONTACT / TIMELINE ──────────────────────────────────────────────────
    {
        "id": "contact-001",
        "title": "How to Contact the Ciocca Center",
        "source": "https://www.scu.edu/cioccacenter/contact-us/",
        "category": "contact",
        "tags": ["contact", "email", "reach out", "ciocca center"],
        "content": (
            "To contact the Ciocca Center for Innovation and Entrepreneurship: "
            "Visit the Contact Us page at https://www.scu.edu/cioccacenter/contact-us/. "
            "You can also join the Ciocca Center email list to stay updated on "
            "programs and application deadlines. "
            "For BEACH specifically, use the application forms: "
            "Client Application: https://share.hsforms.com/1mVfaWY8wSq6huE9FkON6AAcbc5l "
            "Student Application: https://share.hsforms.com/1yUrWjxkiTM26VnwYa84HzAcbc5l "
            "Mentor Application: https://share.hsforms.com/17Nq4WoFuRmuS8Z4Xzl8DXgcbc5l "
            "The center is located at Santa Clara University, Leavey School of Business."
        ),
    },
    {
        "id": "contact-002",
        "title": "BEACH Application Timeline",
        "source": "https://www.scu.edu/cioccacenter/students/beach/",
        "category": "contact",
        "tags": ["timeline", "when", "deadline", "session", "schedule"],
        "content": (
            "BEACH operates in sessions tied to the SCU academic calendar. "
            "Applications open at the start of each new BEACH cohort cycle. "
            "To find current deadlines: visit https://www.scu.edu/cioccacenter/students/beach/ "
            "or join the Ciocca Center email list at "
            "https://www.scu.edu/cioccacenter/contact-us/. "
            "Clients are advised to apply as early as possible as BEACH has "
            "limited capacity per session (approximately 80 clients per year, "
            "with 10 student teams of 4 students each)."
        ),
    },

    # ── PRIVACY ────────────────────────────────────────────────────────────
    {
        "id": "privacy-001",
        "title": "Privacy and Confidentiality in BEACH",
        "source": "https://www.scu.edu/cioccacenter/students/beach/businesses/",
        "category": "privacy",
        "tags": ["privacy", "confidentiality", "NDA", "information sharing"],
        "content": (
            "BEACH is not a formal legal engagement. While student teams work "
            "diligently on client research, BEACH is an educational program. "
            "Clients should be aware that BEACH is operated under SCU's academic "
            "framework. For sensitive business information, clients are encouraged "
            "to consult with licensed legal counsel for formal confidentiality "
            "protections. BEACH teams are guided by mentors and faculty, and "
            "client information is handled respectfully within the program's "
            "educational scope. For specific privacy concerns, contact the "
            "Ciocca Center directly at https://www.scu.edu/cioccacenter/contact-us/."
        ),
    },

    # ── FAQ SEEDS ──────────────────────────────────────────────────────────
    {
        "id": "faq-001",
        "title": "Is BEACH really free?",
        "source": "https://www.scu.edu/cioccacenter/students/beach/businesses/",
        "category": "scope",
        "tags": ["free", "cost", "no charge", "pricing"],
        "content": (
            "Yes, BEACH is completely free for clients. The service is offered "
            "at no charge to small businesses and startups. BEACH is funded by "
            "SCU's Ciocca Center and is part of an educational program where "
            "students gain hands-on experience. There are no hidden fees or "
            "charges for receiving information and resources through BEACH."
        ),
    },
    {
        "id": "faq-002",
        "title": "What happens at a Discovery Meeting?",
        "source": "https://www.scu.edu/cioccacenter/students/beach/",
        "category": "intake",
        "tags": ["discovery meeting", "first meeting", "intake", "process"],
        "content": (
            "The Discovery Meeting is the initial meeting between the BEACH "
            "student team and the client. During this meeting, students learn "
            "about the client's business, understand their specific legal or "
            "business challenge, ask clarifying questions, and define the scope "
            "of research they will conduct. Clients should come prepared to "
            "describe their business, their challenge, and what outcomes they "
            "are hoping to achieve. Commitment to attending this meeting is "
            "required from clients."
        ),
    },
    {
        "id": "faq-003",
        "title": "Can BEACH help with IP / intellectual property questions?",
        "source": "https://www.scu.edu/cioccacenter/students/beach/",
        "category": "scope",
        "tags": ["IP", "intellectual property", "trademark", "patent", "copyright"],
        "content": (
            "Yes, BEACH can provide information and resources on intellectual "
            "property topics including trademarks, patents, copyrights, and "
            "trade secrets. However, BEACH provides informational resources "
            "only — not formal legal advice. For filing patents or trademarks, "
            "or for legal representation, clients should consult a licensed "
            "patent attorney or IP lawyer. BEACH can point clients to USPTO "
            "resources and provide background research to help them understand "
            "their IP situation."
        ),
    },
    {
        "id": "faq-004",
        "title": "Can BEACH help with business formation (LLC, Corp)?",
        "source": "https://www.scu.edu/cioccacenter/students/beach/",
        "category": "scope",
        "tags": ["LLC", "corporation", "business formation", "entity", "structure"],
        "content": (
            "BEACH can provide information and resources about different business "
            "entity structures such as sole proprietorships, LLCs, S-Corps, "
            "C-Corps, and partnerships. Students can research pros/cons, tax "
            "implications, and formation steps for each structure. However, "
            "BEACH cannot formally advise you on which structure to choose "
            "(that is legal/financial advice). The information BEACH provides "
            "helps clients make more informed decisions when they consult with "
            "a licensed attorney or accountant."
        ),
    },
    {
        "id": "faq-005",
        "title": "How is BEACH different from hiring a lawyer?",
        "source": "https://www.scu.edu/cioccacenter/students/beach/businesses/",
        "category": "scope",
        "tags": ["lawyer", "attorney", "difference", "legal counsel"],
        "content": (
            "BEACH is fundamentally different from hiring an attorney. BEACH "
            "provides free information and resources gathered through student "
            "research — it is not legal advice and creates no attorney-client "
            "relationship. A licensed attorney provides formal legal advice, "
            "can represent you in legal proceedings, and carries professional "
            "liability. BEACH is best used to understand a topic, gather "
            "background information, and identify next steps — not as a "
            "substitute for professional legal counsel when legal advice is needed."
        ),
    },
    {
        "id": "faq-006",
        "title": "What is the Bronco Ventures Accelerator?",
        "source": "https://www.scu.edu/cioccacenter/bronco-ventures/bronco-venture-accelerator/",
        "category": "programs",
        "tags": ["bronco ventures", "accelerator", "program", "startup", "launch"],
        "content": (
            "The Bronco Ventures Accelerator is a Ciocca Center program that "
            "supports entrepreneurs from ideation through launch. It is open to "
            "SCU students, faculty, staff, and alumni. The accelerator provides "
            "structured programming, mentorship, resources, and a community of "
            "like-minded entrepreneurs. It culminates in Demo Day, where teams "
            "present their ventures to investors and the broader SCU community. "
            "Sub-programs include Accelerator Prep School and Idea Lab for "
            "earlier-stage founders."
        ),
    },
    {
        "id": "faq-007",
        "title": "Does BEACH help with fundraising or investor pitch?",
        "source": "https://www.scu.edu/cioccacenter/students/beach/",
        "category": "scope",
        "tags": ["fundraising", "investors", "pitch", "VC", "funding"],
        "content": (
            "BEACH can provide information and resources on fundraising topics "
            "including types of funding (bootstrapping, angels, VC, grants), "
            "investor readiness basics, and pitch deck structure. For hands-on "
            "pitch practice and investor connections, the Ciocca Center's "
            "Bronco Ventures programs (Business Pitch Competition, Venture "
            "Capital Competition) are more appropriate. BEACH focuses on "
            "research-backed information rather than direct investor introductions."
        ),
    },
    {
        "id": "faq-008",
        "title": "How many clients does BEACH serve per year?",
        "source": "https://www.scu.edu/cioccacenter/students/beach/",
        "category": "scope",
        "tags": ["capacity", "clients", "how many", "slots"],
        "content": (
            "BEACH serves up to approximately 80 clients per year. The program "
            "runs with approximately 10 student teams per session, and each team "
            "advises up to 4 clients per session. Because capacity is limited, "
            "applicants are encouraged to apply early when applications open "
            "for each BEACH cohort."
        ),
    },
]

# ── HELPER: Simple keyword-based retrieval ──────────────────────────────────

def get_all_chunks():
    """Return full knowledge base."""
    return KNOWLEDGE_BASE


def retrieve_chunks(query: str, top_k: int = 3) -> list[dict]:
    """
    Simple TF-IDF-style keyword retrieval.
    Returns top_k most relevant chunks for the query.
    """
    query_lower = query.lower()
    query_words = set(query_lower.split())

    scored = []
    for chunk in KNOWLEDGE_BASE:
        score = 0
        text = (chunk["content"] + " " + chunk["title"] + " " + " ".join(chunk["tags"])).lower()
        text_words = set(text.split())

        # Exact phrase bonus
        if query_lower in text:
            score += 10

        # Word overlap
        overlap = query_words & text_words
        score += len(overlap) * 2

        # Tag match bonus
        for tag in chunk["tags"]:
            if tag in query_lower:
                score += 5

        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [chunk for _, chunk in scored[:top_k]]
