#!/usr/bin/env python3
"""
Improved CV generation script for Yanan Wu's website
Properly extracts publications and presentations with better parsing
"""

import re
import os
from datetime import datetime

def extract_personal_info(html_content):
    """
    Extract personal information from HTML
    """
    personal_info = {}
    
    # Extract name
    name_pattern = r'<h4>([^<]+)<br>（中文名：[^<]+）</h4>'
    name_match = re.search(name_pattern, html_content)
    if name_match:
        personal_info['name'] = name_match.group(1).strip()
    
    # Extract title/position
    title_pattern = r'<h4>Assistant Professor</h4>'
    if re.search(title_pattern, html_content):
        personal_info['title'] = 'Assistant Professor'
    
    # Extract institution
    institution_pattern = r'<h4>Department of Geography, Central Arkansas University<h4>'
    if re.search(institution_pattern, html_content):
        personal_info['institution'] = 'Department of Geography, Central Arkansas University'
    
    # Extract email
    email_pattern = r'href="mailto:([^"]+)"'
    email_match = re.search(email_pattern, html_content)
    if email_match:
        personal_info['email'] = email_match.group(1)
    
    # Extract address from footer
    address_pattern = r'<p>201 Donaghey Ave,<br> Conway, AR 72035</p>'
    address_match = re.search(address_pattern, html_content)
    if address_match:
        personal_info['address'] = '201 Donaghey Ave, Conway, AR 72035'
    
    return personal_info

def extract_education(html_content):
    """
    Extract education information from HTML
    """
    education = []
    
    # Find education section
    education_pattern = r'<h2 class="section-heading">Education</h2>.*?<p class="large">(.*?)</p>'
    education_match = re.search(education_pattern, html_content, re.DOTALL)
    
    if education_match:
        education_text = education_match.group(1)
        
        # Parse Ph.D.
        phd_pattern = r'&bull; 2019–2024 &emsp; Ph\.D\. in Geospatial information sciences\.\s*<a[^>]*>([^<]+)</a>,\s*([^<]+)'
        phd_match = re.search(phd_pattern, education_text)
        if phd_match:
            education.append({
                'degree': 'Ph.D. in Geospatial Information Sciences',
                'institution': phd_match.group(1).strip(),
                'period': '2019–2024',
                'location': phd_match.group(2).strip()
            })
        
        # Parse M.A.
        ma_pattern = r'&bull; 2017–2019 &emsp; M\.A\. in Geography\.\s*<a[^>]*>([^<]+)</a>,\s*([^<]+)'
        ma_match = re.search(ma_pattern, education_text)
        if ma_match:
            education.append({
                'degree': 'M.A. in Geography',
                'institution': ma_match.group(1).strip(),
                'period': '2017–2019',
                'location': ma_match.group(2).strip()
            })
        
        # Parse B.S.
        bs_pattern = r'&bull; 2013–2017 &emsp; B\.S\. in Resource Environment and Urban-Rural Planning Management\.\s*<a[^>]*>([^<]+)</a>,\s*([^<]+)'
        bs_match = re.search(bs_pattern, education_text)
        if bs_match:
            education.append({
                'degree': 'B.S. in Resource Environment and Urban-Rural Planning Management',
                'institution': bs_match.group(1).strip(),
                'period': '2013–2017',
                'location': bs_match.group(2).strip()
            })
    
    return education

def extract_appointments(html_content):
    """
    Extract appointments/positions from HTML
    """
    appointments = []
    
    # Find appointments section
    appointments_pattern = r'<h2 class="section-heading">Appointments</h2>.*?<p class="large">(.*?)</p>'
    appointments_match = re.search(appointments_pattern, html_content, re.DOTALL)
    
    if appointments_match:
        appointments_text = appointments_match.group(1)
        # Split by bullet points
        appointment_items = re.findall(r'&bull; ([^<]+)<br />', appointments_text)
        
        for item in appointment_items:
            if 'Assistant Professor' in item and 'Central Arkansas University' in item:
                appointments.append({
                    'position': 'Assistant Professor',
                    'institution': 'Department of Geography, Central Arkansas University',
                    'period': '2025–now',
                    'location': 'Conway, AR'
                })
            elif 'Visiting Assistant Professor' in item and 'Clark University' in item:
                appointments.append({
                    'position': 'Visiting Assistant Professor',
                    'institution': 'Geography Department, Clark University',
                    'period': '2024–2025',
                    'location': 'Worcester, MA'
                })
            elif 'GIS Analyst' in item:
                appointments.append({
                    'position': 'GIS Analyst',
                    'institution': 'Information Technology Services, City of Lewisville',
                    'period': '2024–2024',
                    'location': 'Lewisville, TX'
                })
            elif 'Teaching Assistant' in item and 'UTD' in item:
                appointments.append({
                    'position': 'Teaching Assistant',
                    'institution': 'Geospatial Information Sciences Department, UTD',
                    'period': '2023-2024',
                    'location': 'University of Texas at Dallas'
                })
            elif 'Instructor' in item and 'UTD' in item:
                appointments.append({
                    'position': 'Instructor',
                    'institution': 'Geospatial Information Sciences Department, UTD',
                    'period': '2021-2023',
                    'location': 'University of Texas at Dallas'
                })
            elif 'Research Assistant' in item and 'UTD' in item:
                appointments.append({
                    'position': 'Research Assistant',
                    'institution': 'Geospatial Information Sciences Department, UTD',
                    'period': '2019-2020',
                    'location': 'University of Texas at Dallas'
                })
            elif 'Graduate Assistant' in item and 'Binghamton' in item:
                appointments.append({
                    'position': 'Graduate Assistant',
                    'institution': 'Geography Department, Binghamton University',
                    'period': '2017-2019',
                    'location': 'Binghamton University'
                })
    
    return appointments

def extract_publications(html_content):
    """
    Extract publications from HTML with improved parsing
    """
    publications = []
    
    # Find publications section with the specific ID
    publications_pattern = r'<ul id="publications-list">(.*?)</ul>'
    publications_match = re.search(publications_pattern, html_content, re.DOTALL)
    
    if publications_match:
        publications_html = publications_match.group(1)
        # Extract individual publication items
        li_pattern = r'<li[^>]*>(.*?)</li>'
        li_matches = re.findall(li_pattern, publications_html, re.DOTALL)
        
        for li_content in li_matches:
            # Clean up the content - remove HTML tags but preserve structure
            clean_content = re.sub(r'<[^>]+>', '', li_content)
            clean_content = re.sub(r'\s+', ' ', clean_content).strip()
            
            # Extract year
            year_pattern = r'\((\d{4})\)'
            year_match = re.search(year_pattern, clean_content)
            year = year_match.group(1) if year_match else 'Unknown'
            
            # Extract journal from the text (look for italicized text)
            journal_pattern = r'<em>([^<]+)</em>'
            journal_match = re.search(journal_pattern, li_content)
            journal = journal_match.group(1).strip() if journal_match else 'Unknown Journal'
            
            # Extract title (everything between the year and the journal)
            # First, get the part after the year
            after_year_pattern = r'\((\d{4})\)\.\s*<a[^>]*>([^<]+)</a>\.\s*<em>'
            after_year_match = re.search(after_year_pattern, li_content)
            if after_year_match:
                title = after_year_match.group(2).strip()
            else:
                # Fallback: extract title from clean content
                title_pattern = r'\((\d{4})\)\.\s*([^.]+)\.'
                title_match = re.search(title_pattern, clean_content)
                title = title_match.group(2).strip() if title_match else 'Unknown Title'
            
            # Extract authors (everything before the year)
            authors_pattern = r'^([^(]+)'
            authors_match = re.search(authors_pattern, clean_content)
            authors = authors_match.group(1).strip() if authors_match else 'Unknown Authors'
            
            publications.append({
                'year': year,
                'title': title,
                'journal': journal,
                'authors': authors
            })
    
    return publications

def extract_conference_proceedings(html_content):
    """
    Extract conference proceedings from HTML
    """
    proceedings = []
    
    # Find conference proceedings section
    proceedings_pattern = r'<h2 class="section-heading">Conference Proceedings</h2>.*?<ul>(.*?)</ul>'
    proceedings_match = re.search(proceedings_pattern, html_content, re.DOTALL)
    
    if proceedings_match:
        proceedings_html = proceedings_match.group(1)
        # Extract individual proceeding items
        li_pattern = r'<li[^>]*>(.*?)</li>'
        li_matches = re.findall(li_pattern, proceedings_html, re.DOTALL)
        
        for li_content in li_matches:
            # Clean up the content
            clean_content = re.sub(r'<[^>]+>', '', li_content)
            clean_content = re.sub(r'\s+', ' ', clean_content).strip()
            
            # Extract year
            year_pattern = r'(\d{4})'
            year_match = re.search(year_pattern, clean_content)
            year = year_match.group(1) if year_match else 'Unknown'
            
            # Extract title from link
            title_pattern = r'<a[^>]*>([^<]+)</a>'
            title_match = re.search(title_pattern, li_content)
            title = title_match.group(1).strip() if title_match else clean_content
            
            # Extract authors (everything before the link)
            authors_pattern = r'^([^<]+)'
            authors_match = re.search(authors_pattern, clean_content)
            authors = authors_match.group(1).strip() if authors_match else 'Unknown Authors'
            
            proceedings.append({
                'year': year,
                'title': title,
                'authors': authors
            })
    
    return proceedings

def extract_awards(html_content):
    """
    Extract awards and honors from HTML
    """
    awards = []
    
    # Find awards section
    awards_pattern = r'<h2 class="section-heading">Awards and Honors</h2>.*?<div class="container">(.*?)</div>'
    awards_match = re.search(awards_pattern, html_content, re.DOTALL)
    
    if awards_match:
        awards_html = awards_match.group(1)
        
        # Extract awards by year
        year_pattern = r'<h3>(\d{4})</h3>\s*<ul>(.*?)</ul>'
        year_matches = re.findall(year_pattern, awards_html, re.DOTALL)
        
        for year, year_content in year_matches:
            # Extract individual awards
            li_pattern = r'<li[^>]*>(.*?)</li>'
            li_matches = re.findall(li_pattern, year_content, re.DOTALL)
            
            for li_content in li_matches:
                # Clean up the content
                clean_content = re.sub(r'<[^>]+>', '', li_content)
                clean_content = re.sub(r'\s+', ' ', clean_content).strip()
                
                awards.append({
                    'year': year,
                    'award': clean_content
                })
    
    return awards

def extract_presentations(html_content):
    """
    Extract presentations from HTML with improved parsing
    """
    presentations = []
    
    # Find all timeline-year divs and their associated content
    year_pattern = r'<div class="timeline-year">(\d{4})</div>'
    year_matches = re.finditer(year_pattern, html_content)
    
    for year_match in year_matches:
        year = year_match.group(1)
        
        # Find the content after this year div
        start_pos = year_match.end()
        
        # Look for the next timeline-year or end of section
        next_year_match = re.search(r'<div class="timeline-year">', html_content[start_pos:])
        if next_year_match:
            end_pos = start_pos + next_year_match.start()
        else:
            # Look for the end of the presentation-timeline section
            end_match = re.search(r'</div>\s*</div>\s*</div>', html_content[start_pos:])
            if end_match:
                end_pos = start_pos + end_match.start()
            else:
                end_pos = len(html_content)
        
        # Extract the content for this year
        year_content = html_content[start_pos:end_pos]
        
        # Find all li elements in this year's content
        li_pattern = r'<li[^>]*>(.*?)</li>'
        li_matches = re.findall(li_pattern, year_content, re.DOTALL)
        
        for li_content in li_matches:
            # Clean up the content
            clean_content = re.sub(r'<[^>]+>', '', li_content)
            clean_content = re.sub(r'\s+', ' ', clean_content).strip()
            
            # Only add non-empty presentations
            if clean_content and len(clean_content.strip()) > 0:
                presentations.append({
                    'year': year,
                    'title': clean_content
                })
    
    return presentations

def generate_cv_html(personal_info, education, appointments, publications, proceedings, awards, presentations):
    """
    Generate CV HTML content
    """
    cv_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CV - {personal_info.get('name', 'Yanan Wu')}</title>
    <meta name="description" content="Curriculum Vitae of {personal_info.get('name', 'Yanan Wu')}, Assistant Professor of Geography at Central Arkansas University. Expert in GIScience, spatial analysis, and transportation geography.">
    <meta name="author" content="{personal_info.get('name', 'Yanan Wu')}">
    <link rel="icon" type="image/x-icon" href="https://uca.edu/geography/wp-content/themes/ursidae/images/favicon.ico">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #666;
            margin-top: 30px;
            border-bottom: 1px solid #ccc;
            padding-bottom: 5px;
        }}
        .contact-info {{
            margin-bottom: 20px;
        }}
        .publication-item, .education-item, .appointment-item, .award-item, .proceeding-item, .presentation-item {{
            margin-bottom: 10px;
            padding-left: 10px;
        }}
        .year {{
            font-weight: bold;
            color: #333;
        }}
        .journal {{
            font-style: italic;
        }}
        .organization {{
            font-weight: bold;
        }}
        .award-year {{
            font-weight: bold;
            color: #666;
            margin-top: 15px;
        }}
    </style>
</head>
<body>
    <h1>{personal_info.get('name', 'Yanan Wu')}</h1>
    
    <div class="contact-info">
        <p><strong>Email:</strong> {personal_info.get('email', 'yananwu@uca.edu')}</p>
        <p><strong>Address:</strong> {personal_info.get('address', '201 Donaghey Ave, Conway, AR 72035')}</p>
        <p><strong>Position:</strong> {personal_info.get('title', 'Assistant Professor')}</p>
        <p><strong>Institution:</strong> {personal_info.get('institution', 'Department of Geography, Central Arkansas University')}</p>
    </div>
"""
    
    # Add Education section
    cv_html += """
    <h2>Education</h2>
"""
    for edu in education:
        cv_html += f"""
    <div class="education-item">
        <span class="year">{edu['period']}</span> - {edu['degree']}<br>
        {edu['institution']}, {edu['location']}
    </div>
"""
    
    # Add Appointments section
    cv_html += """
    <h2>Appointments</h2>
"""
    for appt in appointments:
        cv_html += f"""
    <div class="appointment-item">
        <span class="year">{appt['period']}</span> - {appt['position']}<br>
        {appt['institution']}, {appt['location']}
    </div>
"""
    
    # Add Publications section
    cv_html += """
    <h2>Publications</h2>
"""
    for pub in publications:
        cv_html += f"""
    <div class="publication-item">
        <span class="year">{pub['year']}</span> - {pub['authors']}<br>
        {pub['title']}<br>
        <span class="journal">{pub['journal']}</span>
    </div>
"""
    
    # Add Conference Proceedings section
    cv_html += """
    <h2>Conference Proceedings</h2>
"""
    for proc in proceedings:
        cv_html += f"""
    <div class="proceeding-item">
        <span class="year">{proc['year']}</span> - {proc['authors']}<br>
        {proc['title']}
    </div>
"""
    
    # Add Awards & Honors section
    cv_html += """
    <h2>Awards & Honors</h2>
"""
    current_year = None
    for award in awards:
        if award['year'] != current_year:
            current_year = award['year']
            cv_html += f"""
    <div class="award-year">{current_year}</div>
"""
        cv_html += f"""
    <div class="award-item">
        • {award['award']}
    </div>
"""
    
    # Add Presentations section
    cv_html += """
    <h2>Presentations</h2>
"""
    current_year = None
    for pres in presentations:
        if pres['year'] != current_year:
            current_year = pres['year']
            cv_html += f"""
    <div class="award-year">{current_year}</div>
"""
        cv_html += f"""
    <div class="presentation-item">
        • {pres['title']}
    </div>
"""
    
    cv_html += """
</body>
</html>
"""
    
    return cv_html

def main():
    """
    Main function to generate CV from HTML content
    """
    html_file = 'index.html'
    cv_file = 'cv.html'
    
    if not os.path.exists(html_file):
        print(f"Error: {html_file} not found!")
        return
    
    print("Reading HTML content...")
    
    # Read HTML content
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print("Extracting information from HTML...")
    
    # Extract information from HTML
    personal_info = extract_personal_info(html_content)
    education = extract_education(html_content)
    appointments = extract_appointments(html_content)
    publications = extract_publications(html_content)
    proceedings = extract_conference_proceedings(html_content)
    awards = extract_awards(html_content)
    presentations = extract_presentations(html_content)
    
    print(f"Extracted {len(education)} education entries")
    print(f"Extracted {len(appointments)} appointments")
    print(f"Extracted {len(publications)} publications")
    print(f"Extracted {len(proceedings)} conference proceedings")
    print(f"Extracted {len(awards)} awards")
    print(f"Extracted {len(presentations)} presentations")
    
    # Print some sample data for debugging
    print("\nSample publications:")
    for i, pub in enumerate(publications[:3]):
        print(f"  {i+1}. {pub['authors']} ({pub['year']}) - {pub['title']}")
    
    print("\nSample presentations:")
    for i, pres in enumerate(presentations[:3]):
        print(f"  {i+1}. ({pres['year']}) - {pres['title']}")
    
    # Generate CV HTML
    print("\nGenerating CV HTML...")
    cv_html = generate_cv_html(personal_info, education, appointments, publications, proceedings, awards, presentations)
    
    # Write CV to file
    with open(cv_file, 'w', encoding='utf-8') as f:
        f.write(cv_html)
    
    print(f"Successfully generated CV: {cv_file}")
    print(f"CV contains {len(education)} education entries, {len(appointments)} appointments, {len(publications)} publications, {len(proceedings)} proceedings, {len(awards)} awards, and {len(presentations)} presentations")

if __name__ == "__main__":
    main()
