from django.shortcuts import render
from markdown2 import Markdown

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    md_entries = util.list_entries()
    # If an entry does not exist, display error page -> requested page was not found.
    if title not in md_entries:
        return render(request, "encyclopedia/error.html", {
            "error_message": f"{title} page was not found"
        })
    # If the entry does exist, display the content of the entry. 
    else:
        md_content = util.get_entry(title)
        markdowner = Markdown()
        html_content = markdowner.convert(md_content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

