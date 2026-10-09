# web

Cynthia Rico Cook: websites and web tools for your business.

- English: https://ricocynthia.github.io/web/
- Español: https://ricocynthia.github.io/web/es/

## How it's put together

| File | What it is |
|---|---|
| `src/page.html` | The one source file. Edit this. |
| `build.py` | Turns the source into the two pages below. |
| `index.html` | English page. Generated, do not edit by hand. |
| `es/index.html` | Spanish page. Generated, do not edit by hand. |
| `img/` | Photos, plus `og.jpg`, the picture shown when the link is shared. |
| `favicon.svg` | The small icon in the browser tab. |
| `sitemap.xml` | Tells search engines about both pages. |

## Changing the text

In `src/page.html`, English text sits inside each element and its Spanish version sits on the same element's `data-es` attribute:

```html
<h3 data-es="Sitios web">Websites</h3>
```

Page titles, descriptions, and the details Google reads are at the top of `build.py`.

After editing, rebuild and push:

```
pip install beautifulsoup4
python3 build.py
```
