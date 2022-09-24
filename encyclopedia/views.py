from django.shortcuts import render
import markdown

from . import util

def convertMd2HTML(text):
    content = util.get_entry(text)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)
    markdowner.convert("*boo!*")

def index(request):
    entries: util.list_entries()
    css_file: util.get_entry("CSS")
    coffee: util.get_entry("coffee")
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    htmlContent = convertMd2HTML(title)
    if htmlContent == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry doesn't exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": htmlContent
        })