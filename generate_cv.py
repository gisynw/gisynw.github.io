#!/usr/bin/env python3
"""
Script to generate a professional CV from HTML content
"""

import re
import os
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

    # --- Extract Education ---
    # Find the "Education" h2 heading and get the next <p class="large">
    edu_heading = soup.find(string=re.compile(r"^Education$", re.IGNORECASE))
    if edu_heading:
        edu_section = edu_heading.parent
        para = edu_section.find_next('p', class_='large')
        if para:
            # Split by <br/> tags to get individual entries
            for line in para.get_text('\n').split('\n'):
                line = line.strip().replace("•", "").replace("&bull;", "").strip()
                if line and re.search(r'\d{4}', line):
                    info['education'].append(line)

    # --- Extract Appointments ---
    appt_heading = soup.find(string=re.compile(r"^Appointments$", re.IGNORECASE))
    if appt_heading:
        appt_section = appt_heading.parent
        para = appt_section.find_next('p', class_='large')
        if para:
            for line in para.get_text('\n').split('\n'):
                line = line.strip().replace("•", "").replace("&bull;", "").strip()
                if line and re.search(r'\d{4}', line):
                    info['appointments'].append(line)


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
            
    return info

def generate_cv_html(info):
    """
    Generate the HTML for the CV
    """
    
    # CSS Styles
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;0,900;1,300;1,400&family=Open+Sans:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap');
        
        body {
            font-family: 'Open Sans', Helvetica, Arial, sans-serif;
            color: #333;
            line-height: 1.5;
            max-width: 850px;
            margin: 40px auto;
            padding: 0 20px;
            background-color: #f9f9f9;
        }
        
        .cv-container {
            background-color: white;
            padding: 50px;
            box-shadow: 0 0 15px rgba(0,0,0,0.05);
            border-top: 5px solid #2c3e50;
        }
        
        a {
            color: #2980b9;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        header {
            border-bottom: 2px solid #eee;
            padding-bottom: 20px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }
        
        h1 {
            font-family: 'Merriweather', serif;
            font-size: 32px;
            color: #2c3e50;
            margin: 0 0 10px 0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .title {
            font-size: 18px;
            color: #7f8c8d;
            font-weight: 300;
            margin: 0;
        }
        
        .contact-info {
            text-align: right;
            font-size: 14px;
            color: #555;
        }
        
        .contact-info p {
            margin: 3px 0;
        }
        
        section {
            margin-bottom: 30px;
        }
        
        h2 {
            font-family: 'Merriweather', serif;
            font-size: 20px;
            color: #2c3e50;
            border-bottom: 3px solid #f1f1f1;
            padding-bottom: 8px;
            margin-top: 0;
            margin-bottom: 20px;
            text-transform: uppercase;
            display: inline-block;
            border-bottom-color: #3498db;
        }
        
        .item {
            margin-bottom: 15px;
            display: flex;
        }
        
        .item-year {
            flex: 0 0 120px;
            font-weight: bold;
            color: #7f8c8d;
            font-size: 14px;
            padding-top: 2px;
        }
        
        .item-content {
            flex: 1;
        }
        
        .publication-item {
            margin-bottom: 12px;
            padding-left: 15px;
            border-left: 3px solid #eee;
        }
        
        .publication-item:hover {
            border-left-color: #3498db;
        }
        
        .appointment-item, .education-item {
            margin-bottom: 15px;
        }
        
        @media print {
            body {
                background-color: white;
                margin: 0;
            }
            .cv-container {
                box-shadow: none;
                padding: 0;
                border: none;
            }
            a {
                color: #000;
                text-decoration: none;
            }
        }
    </style>
    """
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{info['name']} - Curriculum Vitae</title>
    {css}
</head>
<body>

<div class="cv-container">
    <header>
        <div>
            <h1>{info['name']}</h1>
            <h3 class="title">{info['title']}</h3>
            <p>Department of Geography<br>Central Arkansas University</p>
        </div>
        <div class="contact-info">
            <p>{info['contact']['email']}</p>
            <p><a href="{info['contact']['website']}">{info['contact']['website']}</a></p>
            <p>{info['contact']['location']}</p>
        </div>
    </header>

    <section>
        <h2>Education</h2>
"""
    # Parse Education strings to separate Year from Content if possible
    # Strings format: "2019–2024: Ph.D. ..."
    for edu in info['education']:
        # Try to split by first colon or common separator
        parts = edu.split(':', 1)
        if len(parts) == 2:
            year = parts[0].strip()
            desc = parts[1].strip()
        else:
            year = ""
            desc = edu
            
        html += f"""
        <div class="item">
            <div class="item-year">{year}</div>
            <div class="item-content">{desc}</div>
        </div>
        """

    html += """
    </section>

    <section>
        <h2>Academic Appointments</h2>
"""
    for appt in info['appointments']:
        parts = appt.split(':', 1)
        if len(parts) == 2:
            year = parts[0].strip()
            desc = parts[1].strip()
        else:
            year = ""
            desc = appt
            
        html += f"""
        <div class="item">
            <div class="item-year">{year}</div>
            <div class="item-content">{desc}</div>
        </div>
        """

    html += """
    </section>

    <section>
        <h2>Publications</h2>
"""
    for pub in info['publications']:
        html += f"""
        <div class="item">
            <div class="item-year">{pub['year']}</div>
            <div class="item-content publication-item">
                {pub['content']}
            </div>
        </div>
        """

    html += """
    </section>
    
    <section>
        <h2>Grants & Awards</h2>
"""
    # Awards are now organized by year as a dictionary
    for year in sorted(info['awards'].keys(), reverse=True):
        awards_list = info['awards'][year]
        for award_text in awards_list:
            html += f"""
        <div class="item">
            <div class="item-year">{year}</div>
            <div class="item-content">{award_text}</div>
        </div>
        """

    html += """
    </section>
    
    <footer>
        <p style="text-align: center; color: #999; font-size: 12px; margin-top: 50px;">
            Last updated: """ + datetime.now().strftime('%B %Y') + """
        </p>
    </footer>

</div>

</body>
</html>
"""
    return html

def main():
    print("Generating Professional CV...")
    info = extract_info_from_html("index.html")
    
    print(f"Extracted: {len(info['education'])} Education, {len(info['appointments'])} Appointments, {len(info['publications'])} Publications")
    
    cv_html = generate_cv_html(info)
    
    with open("cv.html", "w", encoding='utf-8') as f:
        f.write(cv_html)
        
    print("✅ Successfully generated cv.html")

if __name__ == "__main__":
    main()
