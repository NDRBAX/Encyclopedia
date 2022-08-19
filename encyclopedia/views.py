import re
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown

from . import util

markdowner = Markdown()
list_entries = util.list_entries()
lower_list = [entry.lower() for entry in list_entries]


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries
    })

def entry(request, title):
    # If the entry does exist, display the content of the entry
    if title.lower() in lower_list:
        position = lower_list.index(title.lower())
        html_content = markdowner.convert(util.get_entry(list_entries[position]))
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    # If an entry does not exist, display error page requested page was not found
    else:
        return render(request, "encyclopedia/error.html", {
            "error_message": f"{title} page was not found"
        })
      

def search(request):
    query = request.GET.get("q", "")
    filtered_list = []
    # If the query is in the list of entries, display the entry
    if query.lower() in lower_list:
        position = lower_list.index(query.lower())
        return HttpResponseRedirect(reverse("entry", args=[list_entries[position]]))
    # Else, displays a list of all encyclopedia entries that have the query as a substring
    else:
        r = re.compile(f".*{query}", re.IGNORECASE)
        filtered_list = list(filter(r.match, list_entries))
        if len(filtered_list) > 0:
            return render(request, "encyclopedia/index.html", {
                "entries": filtered_list,
            })
        # If no entries are found, display error page
        else:
            return render(request, "encyclopedia/error.html", {
                "error_message": f"{query} was not found"
            })