import json

# === Utility ===

def save_markdown(content, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Markdown file '{filename}' created.")


# === CV ===

def render_cv_markdown(data):
    lines = ["# Curriculum Vitae of Jakob Löber\n"]
    lines.append("PhD in Theoretical Physics | Data Scientist | Augmented Reality\n")

    lines.append("## Professional Background\n")
    for job in data["professional_background"]:
        company = f"[{job['company']}]({job['link']})" if "link" in job else job["company"]
        lines.append(f"**{job['period']}**  \n{job['position']} — *{company}*")
        lines.extend(f"- {d}" for d in job.get("details", []))
        lines.append("")

    lines.append("## Education\n")
    for edu in data["education"]:
        lines.append(f"**{edu['period']}**  \n{edu['degree']} in {edu.get('field', '')} — *{edu['institution']}*")
        if "grade" in edu:
            lines.append(f"- Grade: {edu['grade']}")
        if "focus" in edu:
            lines.append(f"- Focus: {', '.join(edu['focus'])}")
        if "title" in edu:
            lines.append(f"- Title: *{edu['title']}*")
        if "publication" in edu:
            lines.append(f"- Publication: {edu['publication']}")
        if "summary" in edu:
            lines.append(f"- Summary: {edu['summary']}")
        lines.append("")

    lines.append("## Other Activities and Experiences\n")
    for act in data["other_activities_and_experiences"]:
        lines.append(f"**{act['period']}**  \n{act['activity']} — *{act['organization']}*")
        if "topics" in act:
            lines.append(f"- Topics: {', '.join(act['topics'])}")
        lines.extend(f"- {d}" for d in act.get("details", []))
        lines.append("")

    return "\n".join(lines)


# === Skills ===

def score_to_bar(score, max_score=10):
    return f"[{'■' * score}{'□' * (max_score - score)}]"

# def render_skills_markdown(data):
#     lines = ["# Skills Overview\n"]
#     for category, skills in data.items():
#         lines.append(f"## {category}")
#         lines.extend(f"- {score_to_bar(skill['score'])}  {skill['name']}" for skill in skills)
#         lines.append("")
#     return "\n".join(lines)

def render_skills_markdown(data, columns=6):
    lines = ["# Skills Overview\n"]

    categories = list(data.items())

    # Pad the total number of categories to be divisible by `columns`
    while len(categories) % columns != 0:
        categories.append(("", []))

    # Split into chunks of `columns` categories
    category_chunks = [
        categories[i:i + columns]
        for i in range(0, len(categories), columns)
    ]

    for chunk in category_chunks:
        lines.append("<table><tr>")
        # Headers
        for category, _ in chunk:
            header = f"<strong>{category}</strong>" if category else ""
            lines.append(f"<th align='left' style='padding-right: 20px;'>{header}</th>")
        lines.append("</tr>")

        # Number of skill rows to render = max skills in any category in this chunk
        max_rows = max(len(skills) for _, skills in chunk)

        for i in range(max_rows):
            lines.append("<tr>")
            for _, skills in chunk:
                if i < len(skills):
                    skill = skills[i]
                    lines.append(
                        "<td style='padding-right: 20px;'>"
                        f"{score_to_bar(skill['score'])}<br>"
                        f"{skill['name']}"
                        "</td>"
                    )
                else:
                    lines.append("<td></td>")
            lines.append("</tr>")

        lines.append("</table>\n")  # space between tables

    return "\n".join(lines)


# === Publications ===

def decode_latex_accents(text):
    replacements = {
        r'\"a': 'ä', r'\"o': 'ö', r'\"u': 'ü', r'\"A': 'Ä', r'\"O': 'Ö', r'\"U': 'Ü',
        r'\"e': 'ë', r'\"i': 'ï', r'\"E': 'Ë', r'\"I': 'Ï',
        r'\\"a': 'ä', r'\\"o': 'ö', r'\\"u': 'ü', r'\\"A': 'Ä', r'\\"O': 'Ö', r'\\"U': 'Ü',
        r'\\"e': 'ë', r'\\"i': 'ï', r'\\"E': 'Ë', r'\\"I': 'Ï',
        r'\ss{}': 'ß', r'\~n': 'ñ', r'\~N': 'Ñ', r'\`e': 'è', r"\'e": 'é', r'\`a': 'à',
        r'\`u': 'ù', r"\'a": 'á', r"\'o": 'ó', r"\'u": 'ú',
        r'\{': '', r'\}': '', r'~': '', r'--': '–', r'---': '—', r'\\': ''
    }
    for latex, char in replacements.items():
        text = text.replace(latex, char)
    return text

def render_publications_markdown(data):
    lines = [f"# Publications ({len(data)})\n"]
    for i, pub in enumerate(data, 1):
        authors = decode_latex_accents(pub["authors"].strip().rstrip(","))
        title = decode_latex_accents(pub["title"])
        journal = decode_latex_accents(pub["journal"])
        url = pub["url"]
        lines.append(f"{i}. **{title}**  \n   *{authors}*  \n   *{journal}*  \n   [Link to article]({url})\n")
    return "\n".join(lines)


# === Thesis ===

def render_thesis_markdown(data):
    def section(title): return f"\n## {title}\n"
    def bold(label, value): return f"**{label}:** {value}  \n"
    def link(text, url): return f"[{text}]({url})"
    def render_supervisors(supervisors):
        return ", ".join(link(s['name'], s['link']) for s in supervisors)

    md = ["# Academic Theses\n"]
    dt = data["doctoral_thesis"]
    md.append(section("Doctoral Thesis"))
    md.append(bold("Title", link(dt["title"], dt["pdf_link"])))
    md.append(bold("Supervisors", render_supervisors(dt["supervisors"])))
    md.append(bold("Date of Defence", dt["date_of_defence"]))
    md.append(bold("Defence Talk", link(dt["defence_talk"]["title"], dt["defence_talk"]["pdf_link"])))
    md.append("**Abstract:**\n" + dt["abstract"] + "\n")

    dip = data["diploma_thesis"]
    md.append(section("Diploma Thesis"))
    md.append(bold("Title", link(dip["title"], dip["pdf_link"])))
    md.append(bold("Supervisors", render_supervisors(dip["supervisors"])))
    md.append("**Abstract:**\n" + dip["abstract"] + "\n")

    return "\n".join(md)


# === Presentations ===

def render_presentations_markdown(data):
    lines = [f"# Scientific Presentations ({len(data)})\n"]
    for i, t in enumerate(data, 1):
        lines.append(f"{i}. [{t['title']}]({t['link']})  \n   _{t['event']}_")
    return "\n\n".join(lines)


# === Posters ===

def render_posters_markdown(data):
    lines = [f"# Posters ({len(data)})\n"]
    for i, p in enumerate(data, 1):
        lines.append(f"{i}. [{p['title']}]({p['link']})  \n   _{p['event']}_")
    return "\n\n".join(lines)


# === Combine All Sections ===

def render_full_cv(cv_data, skills_data, publications_data, thesis_data, presentations_data, posters_data, to_file=None):
    def collapsible(title, content):
        return f"<details>\n<summary>{title}</summary>\n\n{content}\n</details>\n"

    parts = [
        render_cv_markdown(cv_data),
        collapsible("Skills Overview", render_skills_markdown(skills_data)),
        collapsible("Publications", render_publications_markdown(publications_data)),
        collapsible("Academic Theses", render_thesis_markdown(thesis_data)),
        collapsible("Scientific Presentations", render_presentations_markdown(presentations_data)),
        collapsible("Posters", render_posters_markdown(posters_data)),
    ]

    output = "\n\n".join(parts)
    if to_file:
        save_markdown(output, to_file)
    return output


# === Load Data and Generate Files ===

cv_data = json.load(open("data/cv.json"))
skills_data = json.load(open("data/skills.json"))
publications_data = json.load(open("data/publications.json"))
thesis_data = json.load(open("data/thesis.json"))
presentations_data = json.load(open("data/presentations.json"))
posters_data = json.load(open("data/posters.json"))

render_full_cv(
    cv_data,
    skills_data,
    publications_data,
    thesis_data,
    presentations_data,
    posters_data,
    to_file="full_cv.md"
)

render_full_cv(
    cv_data,
    skills_data,
    publications_data,
    thesis_data,
    presentations_data,
    posters_data,
    to_file="README.md"
)
