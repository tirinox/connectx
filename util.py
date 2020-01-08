import os
import tempfile


def show_html(html):
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', delete=False, suffix='.html') as f:
        f.write(html)
        os.system(f'open {f.name}')