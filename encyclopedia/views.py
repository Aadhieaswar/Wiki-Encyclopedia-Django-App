from django.shortcuts import render, redirect

import markdown as md

from .forms import CreateEntry
from . import util

def index(request):
    context = {
        "entries": util.list_entries(),
    }
    return render(request, "encyclopedia/index.html", context)

def wiki(request, entry):
    if entry not in util.list_entries():
        return redirect("encyclopedia:home")
    content = util.get_entry(entry)

    html = md.markdown(content, safe_mode=True)

    context = {
        "entries": util.list_entries(),
        "entry": entry,
        "content": html,
    }
    return render(request, "encyclopedia/index.html", context)

def search(request):
    if request.method == "POST":
        results = []

        key = request.POST["key"].replace(" ", "")
        entries = util.list_entries()

        for entry in entries:
            if key.lower() in entry.lower():
                results.append(entry)

        if len(results) > 0:
            message = "Results Found"
        else:
            message = "Sorry, we were not able to find any results for your search<p class=\"not-found-msg\">Try using any other keywords or check your search for spellling errors</p>"
        context = {
            "results": results,
            "message": message,
            "key": key,
        }
        return render(request, "encyclopedia/results.html", context)
    return redirect("encyclopedia:home")

def createNew(request):
    if request.method == "POST":
        form = CreateEntry(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            title = title.capitalize()
            content = form.cleaned_data['content']

            if title in util.list_entries():
                form = CreateEntry(initial={'content': content})
                content = {
                    "form": form,
                    "err_msg": "Title entered already exists! Please try a different name.",
                }
                return render(request, "encyclopedia/entry.html", content)
            else:
                util.save_entry(title, content)
                return redirect("encyclopedia:wiki", title)
        return render(request, "encyclopedia/entry.html", context)
    form = CreateEntry()
    context = {
        "form": form,
    }
    return render(request, "encyclopedia/entry.html", context)

def editEntry(request, entry):
    if entry not in util.list_entries():
        return redirect("encyclopedia:home")
    if request.method == 'POST':
        content = request.POST["new_content"]
        util.save_entry(entry, content)
        context = {
            "entry": entry,
            "content": content,
            "success": "Successfully Saved Changes",
        }
        return render(request, "encyclopedia/editor.html", context)
    textcontent = util.get_entry(entry)
    context = {
        "entry": entry,
        "content": textcontent,
    }
    return render(request, "encyclopedia/editor.html", context)
