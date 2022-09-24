from urllib import request
from django.shortcuts import render
import markdown
import random

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

def search(request):
    if request.method == "POST":
        entrySearch = request.POST['q']
        htmlContent = convertMd2HTML(entrySearch)
        if htmlContent is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entrySearch,
                "content": htmlContent
            })
        else:
            allEntries = util.list_entries()
            recommendations = []
            for entry in allEntries:
                if entrySearch.lower() in entry.lower():
                    recommendations.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendations": recommendations
            })

def newPage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        isTitle = util.get_entry(title)
        if isTitle is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry page already exist"
            })
        else:
            util.save_entry(title, content)
            htmlContent = convertMd2HTML(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": htmlContent, 
            })

def editPage(request):
    if request.method == "POST":
        title = request.POST['entryTitle']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def saveEdit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        htmlContent = convertMd2HTML(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": htmlContent, 
        })

def rand(request):
    allEntries = util.list_entries()
    randomEntry = random.choice(allEntries)
    htmlContent = convertMd2HTML(randomEntry)
    return render(request, "encyclopedia/entry.html", {
        "title": randomEntry,
        "content": htmlContent, 
    })