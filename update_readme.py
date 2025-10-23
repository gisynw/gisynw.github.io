#!/usr/bin/env python3
"""
Script to update README.md with basic information
"""

import os
from datetime import datetime

def update_readme():
    """
    Update README.md with current information
    """
    readme_content = """# Yanan Wu's Personal Website

This repository contains the source code for Yanan Wu's personal academic website. Yanan Wu is an Assistant Professor in the Department of Geography at Central Arkansas University, specializing in Geospatial Information Sciences.

## About the Website

This website serves as a professional portfolio showcasing academic journey, research projects, publications, and teaching experience. It features a modern, responsive design with smooth animations and interactive elements.

## Website Sections

- **About Me**
  - Professional background
  - Education history
  - Academic appointments
  - Contact information

- **Research & Projects**
  - GIScience research
  - Tools & Addins development
  - WebGIS applications
  - Interactive project showcases

- **Academic Information**
  - Publications
  - Teaching experience
  - Awards and honors
  - Conference presentations

## Contact Information

- **Email**: yananwu@uca.edu
- **GitHub**: [gisynw](https://github.com/gisynw)
- **LinkedIn**: [giswu](https://www.linkedin.com/in/giswu/)
- **Medium**: [ywu120766](https://ywu120766.medium.com/)
- **Faculty Page**: [Central Arkansas University](https://uca.edu/geography/faculty/yanan-wu/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
"""

    # Write the updated README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("Successfully updated README.md")
    print("Updated information:")
    print("- Position: Assistant Professor at Central Arkansas University")
    print("- Email: yananwu@uca.edu")
    print("- Faculty page link updated")
    print("- Removed 'Dr.' title for humility")

def main():
    """
    Main function to update README
    """
    if not os.path.exists('README.md'):
        print("README.md not found!")
        return
    
    print("Updating README.md...")
    update_readme()

if __name__ == "__main__":
    main()
