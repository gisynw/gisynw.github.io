"""Run with python test_generate_cv.py."""
from pathlib import Path
from tempfile import TemporaryDirectory
from bs4 import BeautifulSoup
from generate_cv import extract_info_from_html, generate_cv_html


with TemporaryDirectory() as directory:
    source = Path(directory) / 'index.html'
    source.write_text('''<title>Example - CV</title>
        <h2>Education</h2><p class="large">• 2019–2024 Ph.D.
        <a href="#">Example University</a>, USA<br>• 2017–2019 M.A.</p>
        <h2>Appointments</h2><p class="large">• 2025–now Professor,
        Geography Department</p>
        <section id="service"><h3>2026</h3><ul><li>Paper judge</li></ul>
        <h3>2022</h3><ul><li>Student assistant</li></ul></section>
        <section id="grants"><h3>External Grants</h3><ul><li>Travel grant</li></ul></section>
        ''', encoding='utf-8')
    info = extract_info_from_html(source)
    assert info['education'] == ['2019–2024 Ph.D. Example University, USA', '2017–2019 M.A.']
    assert info['appointments'] == ['2025–now Professor, Geography Department']
    page = BeautifulSoup(generate_cv_html(info), 'html.parser')
    assert [node.get_text() for node in page.select('.date')] == ['2019–2024', '2017–2019', '2025–now']
    assert [node.get_text() for node in page.select('.year')] == ['2026', '2022']
    assert 'Travel grant' in page.get_text()
    assert 'Paper judge' in page.get_text()
print('CV extraction and rendering checks passed')
