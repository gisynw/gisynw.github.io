#!/usr/bin/env python3
"""
Script to update publications in index.html directly from Google Scholar
using the `scholarly` library.
"""

import sys
import re
from scholarly import scholarly

# Import helper functions from existing script
try:
    from archive.update_publications import update_html_file, generate_html_li
except ImportError:
    print("Error: Could not import from update_publications.py")
    sys.exit(1)

def fetch_and_parse_publications(scholar_id):
    """
    Fetch publications from Google Scholar and parse them into the format
    expected by generate_html_li.
    """
    print(f"Searching for author with ID: {scholar_id}")
    try:
        author = scholarly.search_author_id(scholar_id)
        print(f"Found author: {author.get('name')}")
        
        # Fill publication details (this might take a while and risks blocking if too aggressive)
        # For now, we will try to use available data from the search result 
        # and only fill if strictly necessary, or just rely on what's available to avoid blocking.
        # Ideally, we should use `scholarly.fill(author, sections=['publications'])`
        
        print("Fetching publications list...")
        publications_data = []
        
        # scholarly returns an iterator or list
        # We need to fill the author to get the full list of publications
        
        # NOTE: filling all publications details might be slow and trigger rate limits.
        # We will try to get the full list first.
        pub_list = scholarly.fill(author, sections=['publications'])['publications']
        
        print(f"Found {len(pub_list)} publications. Processing...")
        
        for i, pub in enumerate(pub_list):
            title = pub.get('bib', {}).get('title')
            year = pub.get('bib', {}).get('pub_year')
            
            # Skip if no title or year (minimal requirements)
            if not title:
                continue
                
            # If we need more details (journal, volume, etc.), we might need to fill the publication
            # But this is expensive. Let's try to get what we can.
            # 'bib' usually contains: title, pub_year, citation
            # We might need to fill to get 'journal', 'author', etc.
            
            try:
                # Filling individual publication to get full bibtex
                # We can add a delay if needed, but let's try without first
                filled_pub = scholarly.fill(pub)
                bib = filled_pub['bib']
                
                authors_list = bib.get('author', '').split(' and ')
                # Format authors: "Last, F."
                formatted_authors = []
                for auth in authors_list:
                    parts = auth.strip().split()
                    if not parts:
                        continue
                    if len(parts) == 1:
                        formatted_authors.append(parts[0])
                    else:
                        last_name = parts[-1]
                        initials = ''.join([p[0]+'.' for p in parts[:-1]])
                        formatted_authors.append(f"{last_name}, {initials}")
                
                authors_str = ", ".join(formatted_authors)
                authors_str = authors_str.replace("&", "&amp;") # Basic escape
                
                # Bold Yang, Y.
                authors_final = re.sub(r'Yang, Y\.', '<b>Yang, Y.</b>', authors_str)
                # Also handle variations like "Yang, Y.-L." or just "Yang, Y"
                if "<b>" not in authors_final and "Yang" in authors_str:
                     authors_final = re.sub(r'Yang, [A-ZY]\.?', '<b>Yang, Y.</b>', authors_str)

                # Extract other fields
                journal = bib.get('journal') or bib.get('conference') or bib.get('publisher') or "Unknown Journal"
                volume = bib.get('volume')
                issue = bib.get('number')
                pages = bib.get('pages')
                
                # DOI logic (scholarly doesn't always give DOI, we might need to infer or it might be in 'pub_url' or similar)
                pub_url = filled_pub.get('pub_url')
                doi_url = pub_url if pub_url else None
                
                # Determine type
                pub_type = 'journal'
                if 'thesis' in title.lower() or 'thesis' in journal.lower():
                    pub_type = 'thesis'

                pub_data = {
                    'authors': authors_final,
                    'year': int(year) if year else 0,
                    'title': title,
                    'journal': journal,
                    'volume': volume,
                    'issue': issue,
                    'pages': pages,
                    'doi_url': doi_url,
                    'type': pub_type
                }
                
                publications_data.append(pub_data)
                print(f"  Processed: {title[:50]}...")
                
            except Exception as e:
                print(f"  Error processing publication '{title[:30]}...': {e}")
                continue

        return publications_data

    except Exception as e:
        print(f"Error fetching from Google Scholar: {e}")
        return []

def main():
    scholar_id = "xVDuszoAAAAJ"
    html_file = "index.html"
    
    print(f"Starting update from Google Scholar ID: {scholar_id}")
    
    publications_data = fetch_and_parse_publications(scholar_id)
    
    if not publications_data:
        print("No publications found or error occurred.")
        return

    # Sort by year (newest first)
    publications_data.sort(key=lambda x: x['year'], reverse=True)
    
    print(f"\nCollected {len(publications_data)} publications.")
    
    # Check existing html content to preserve existing ones if needed?
    # Actually, the requirement implies we should generate code directly using scholar id,
    # which implies replacing or merging.
    # The existing logic in update_html_file appends new ones to existing ones unless they exist.
    # But here we are fetching ALL. So we might potential duplicate if we just append.
    # We should probably clear existing or check for duplicates intelligently.
    # `update_html_file` in `update_publications.py` has logic:
    # 1. Reads existing.
    # 2. Merges with new.
    # 3. Sorts.
    # However, if we feed it ALL publications from Scholar, and they are already in HTML,
    # we need to make sure we don't duplicate. 
    # The current `main` in `update_publications.py` checks for duplicates by title.
    # We should do the same here.
    
    # Use helper to extract existing titles
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # We need to import `extract_existing_publications` too, but it wasn't imported above.
    # Let's import it now or Copy it.
    from archive.update_publications import extract_existing_publications
    
    existing_titles = extract_existing_publications(html_content)
    print(f"Found {len(existing_titles)} existing publications in HTML")
    
    new_publications_data = []
    for pub in publications_data:
        # Simple title check (strip punctuation/case for better match?)
        # For now, exact match as in original script
        if pub['title'] in existing_titles:
             # Identify if we want to UPDATE existing entries?
             # The original script skips. We will skip too for safety.
             # print(f"Skipping existing: {pub['title'][:30]}...")
             pass
        else:
             # Check fuzzy match?
             # Sometimes titles vary slightly. 
             # For now, strict match.
             if pub['title'] not in existing_titles:
                 new_publications_data.append(pub)

    if not new_publications_data:
         print("No NEW publications found from Google Scholar (all match existing titles).")
         # Proceed to re-sort anyway?
         # But `update_html_file` expects a list of formatted HTML items.
         return

    print(f"Found {len(new_publications_data)} NEW publications to add.")
    
    # Generate HTML items
    html_items = []
    for pub_data in new_publications_data:
        html_li = generate_html_li(pub_data)
        html_items.append(html_li)
        
    # Read existing publications HTML to pass to update_html_file
    # (Update: update_html_file extracts existing internally? No, it takes `existing_publications_html` argument)
    # create `existing_publications_html`
    existing_publications_html = ""
    ul_start = html_content.find('<ul id="publications-list">')
    if ul_start != -1:
        ul_end = html_content.find('</ul>', ul_start)
        if ul_end != -1:
            existing_publications_html = html_content[ul_start + len('<ul id="publications-list">'):ul_end]

    # Call update
    if update_html_file(html_file, html_items, existing_publications_html):
        print("Successfully updated index.html")
    else:
        print("Failed to update index.html")

if __name__ == "__main__":
    main()
