#!/usr/bin/env python3
"""
Script to generate a professional CV from HTML content
"""

import re
from pathlib import Path
from html import escape
from bs4 import BeautifulSoup
from datetime import datetime

def extract_info_from_html(html_file):
    """
    Extract structured information from index.html using BeautifulSoup
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extract name from title tag
    title_tag = soup.find('title')
    name_match = re.search(r'([A-Za-z\s]+)\s*[-–]', title_tag.string) if title_tag else None
    name = name_match.group(1).strip() if name_match else "Yanan Wu"
    
    # Extract title from og:description or structured data
    description_tag = soup.find('meta', property='og:description')
    title = ""
    if description_tag:
        match = re.search(r'([^.]+)', description_tag.get('content', ''))
        if match:
            title = match.group(1).strip()
    
    info = {
        'name': name,
        'title': title if title else "Assistant Professor of Geography",
        'contact': {
            'email': "ywu@uca.edu",
            'phone': "",
            'office': "",
            'location': "Conway, Arkansas",
            'website': "https://gisynw.github.io"
        },
        'education': [],
        'appointments': [],
        'publications': [],
        'awards': {}
    }

    # Split only on actual line breaks, preserving linked institution names.
    for heading, key in [('Education', 'education'), ('Appointments', 'appointments')]:
        node = soup.find('h2', string=re.compile(r'^' + heading + r'$'))
        para = node.find_next('p', class_='large') if node else None
        if para:
            for fragment in re.split(r'<br\b[^>]*>', para.decode_contents(), flags=re.I):
                line = BeautifulSoup(fragment, 'html.parser').get_text()
                line = re.sub(r'\s+', ' ', line).strip().lstrip('\u2022').strip()
                if line:
                    info[key].append(line)

    # --- Extract Publications ---
    pub_ul = soup.find('ul', id='publications-list')
    if pub_ul:
        for li in pub_ul.find_all('li'):
            text = li.get_text(" ", strip=True)
            text = re.sub(r'\s+', ' ', text)
            
            # Extract Year - look for 4-digit year in parentheses
            year_match = re.search(r'\((\d{4})\)', text)
            year = year_match.group(1) if year_match else "Unknown"
            
            # Keep the full HTML content to preserve links and formatting
            content_html = "".join([str(x) for x in li.contents])
            
            info['publications'].append({
                'year': year,
                'content': content_html,
                'text': text
            })

    # --- Extract Awards ---
    # Awards are organized by year in <h3> tags
    awards_section = soup.find('section', id='awards')
    if awards_section:
        current_year = None
        for element in awards_section.find_all(['h3', 'li']):
            if element.name == 'h3':
                current_year = element.get_text(strip=True)
                if current_year not in info['awards']:
                    info['awards'][current_year] = []
            elif element.name == 'li' and current_year:
                award_text = element.get_text(" ", strip=True)
                award_text = re.sub(r'\s+', ' ', award_text)
                info['awards'][current_year].append(award_text)
            
    info['grants'] = {}
    for heading in soup.select('#grants h3'):
        info['grants'][heading.get_text(strip=True)] = [
            li.decode_contents() for li in heading.find_next('ul').find_all('li')
        ]
    info['service'] = {}
    for heading in soup.select('#service h3'):
        info['service'][heading.get_text(strip=True)] = [
            li.decode_contents() for li in heading.find_next('ul').find_all('li')
        ]
    info['presentations'] = {}
    for item in soup.select('#presentations .timeline-item'):
        year = item.select_one('.timeline-year').get_text(strip=True)
        info['presentations'][year] = [li.decode_contents() for li in item.select('li')]
    info['proceedings'] = []
    for heading in soup.select('#publication h2'):
        if heading.get_text(strip=True) == 'Conference Proceedings':
            for li in heading.find_next('ul').find_all('li'):
                for link in li.select('a'):
                    if not link.get('href'):
                        link.unwrap()
                info['proceedings'].append(li.decode_contents())

    return info

def generate_cv_html(info):
    """Render homepage content using the supplied Word CV's academic layout."""
    def section(title, content):
        return f'<section><h2>{escape(title)}</h2>{content}</section>'

    def dated_entries(entries):
        result = []
        for entry in entries:
            match = re.match(r'^(\d{4}(?:\s*[\u2013\u2014-]\s*(?:\d{4}|now|Present))?)\s*:?\s+(.+)$', entry)
            year, description = match.groups() if match else ('', entry)
            result.append(f'<div class="dated-entry"><div>{escape(description)}</div>'
                          f'<div class="date">{escape(year)}</div></div>')
        return ''.join(result)

    def year_groups(groups, plain=False):
        rows = []
        for year in sorted(groups, reverse=True):
            for index, text in enumerate(groups[year]):
                content = escape(text) if plain else text
                rows.append(f'<div class="year-entry"><div class="year">{escape(year) if index == 0 else ""}</div>'
                            f'<div>{content}</div></div>')
        return ''.join(rows)

    sections = [section('Education', dated_entries(info['education'])),
                section('Appointments', dated_entries(info['appointments']))]
    if info['grants']:
        sections.append(section('Grants', ''.join(
            f'<h3>{escape(label)}</h3><ul>' + ''.join(f'<li>{text}</li>' for text in entries) + '</ul>'
            for label, entries in info['grants'].items())))
    sections.append(section('Publications', ''.join(
        f'<p class="citation">{pub["content"]}</p>' for pub in info['publications'])))
    if info['proceedings']:
        sections.append(section('Conference Proceedings', ''.join(
            f'<p class="citation">{text}</p>' for text in info['proceedings'])))
    for title, key in [('Awards', 'awards'), ('Presentations', 'presentations'), ('Academic Service', 'service')]:
        if info[key]:
            sections.append(section(title, year_groups(info[key], plain=key == 'awards')))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(info['name'])} - Curriculum Vitae</title>
<style>
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #eee; color: #000; font: 11pt/1.25 "Times New Roman", Times, serif; }}
.cv-container {{ max-width: 210mm; margin: 24px auto; padding: 12.7mm; background: #fff; }}
.cv-actions {{ max-width: 210mm; margin: 20px auto; padding: 0 18px; text-align: right; font: 14px/1.5 Arial, sans-serif; }}
.cv-actions button {{ padding: 10px 18px; border: 1px solid #333; border-radius: 4px; background: #333; color: #fff; font: inherit; cursor: pointer; }}
.cv-actions button:hover {{ background: #555; }}
.cv-actions p {{ margin: 6px 0 0; }}
header {{ text-align: center; margin-bottom: 22px; }}
h1 {{ font-size: 16pt; margin: 0 0 7px; text-transform: uppercase; }}
header p {{ margin: 4px 0; }}
a {{ color: inherit; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.profile-links a {{ text-decoration: underline; text-underline-offset: 2px; }}
section {{ margin-top: 18px; }}
h2 {{ font-size: 12pt; text-transform: uppercase; border-bottom: 1px solid #000; margin: 0 0 9px; padding-bottom: 2px; break-after: avoid; }}
h3 {{ font-size: 11pt; margin: 10px 0 6px; break-after: avoid; }}
.dated-entry {{ display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 16px; margin-bottom: 10px; break-inside: avoid; }}
.date {{ text-align: right; white-space: nowrap; }}
.year-entry {{ display: grid; grid-template-columns: 48px minmax(0, 1fr); gap: 12px; margin-bottom: 8px; break-inside: avoid; }}
.citation {{ margin: 0 0 9px; padding-left: 20px; text-indent: -20px; break-inside: avoid; }}
ul {{ margin: 0; padding-left: 20px; }}
li {{ margin-bottom: 8px; }}
footer {{ text-align: center; font-size: 9pt; margin-top: 24px; }}
@page {{ size: A4; margin: 12.7mm; }}
@media print {{
    .cv-actions {{ display: none; }}
    body {{ background: #fff; }}
    .cv-container {{ max-width: none; margin: 0; padding: 0; }}
    p, li {{ orphans: 2; widows: 2; }}
}}
@media screen and (max-width: 600px) {{
    .cv-container {{ margin: 0; padding: 24px 18px; }}
    .dated-entry {{ grid-template-columns: minmax(0, 1fr); gap: 3px; }}
    .date {{ text-align: left; }}
}}
</style>
</head>
<body>
<div class="cv-actions">
<button type="button" onclick="window.print()" aria-describedby="pdf-help">Download as PDF</button>
<p id="pdf-help">Choose “Save as PDF” in the print dialog.</p>
</div>
<main class="cv-container">
<header>
<h1>{escape(info['name'])}</h1>
<p>{escape(info['title'])}</p>
<p><a href="mailto:{escape(info['contact']['email'])}">{escape(info['contact']['email'])}</a> | {escape(info['contact']['location'])}</p>
<p class="profile-links"><a href="{escape(info['contact']['website'])}">Personal Website</a> |
<a href="https://www.linkedin.com/in/giswu/">LinkedIn</a> |
<a href="https://github.com/gisynw">GitHub</a> |
<a href="https://ywu120766.medium.com/">Medium</a></p>
</header>
{''.join(sections)}
<footer>Last updated: {datetime.now().strftime('%B %Y')}</footer>
</main>
</body>
</html>
"""


def main():
    root = Path(__file__).resolve().parent
    info = extract_info_from_html(root / 'index.html')
    (root / 'cv.html').write_text(generate_cv_html(info), encoding='utf-8')
    print('Generated cv.html from index.html')


if __name__ == '__main__':
    main()
