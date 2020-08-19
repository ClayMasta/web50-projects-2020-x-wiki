from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from . import util
import markdown2
import random

class SearchForm(forms.Form):
    q = forms.CharField(label="q")

class NewPageForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="content")

class EditPageForm(forms.Form):
     content = forms.CharField(label="content")

def index(request):
    entries = util.list_entries()
    if request.method == "POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data["q"]
            content = util.get_entry(query)
            if content:
                return redirect("/wiki/" + query)

            else:
                results = []
                count = 0
                for entry in entries:
                    if query.lower() in entry.lower():
                        results.append(entry)
                        count += 1
                return render(request, "encyclopedia/search.html", {
                    "results": results, "count": count, "query": query
                })

    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry(request, title):
    content = util.get_entry(title)
    if content:
        return render(request, "encyclopedia/entry.html", {
            "title": title, "content": markdown2.markdown(content)
        })
    else:
        return HttpResponse(f"404. {title} was not found")

def new(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/created.html", {
                "title": title
            })
                
    return render(request, "encyclopedia/new.html")

def edit(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)

        return redirect("/wiki/" + title)

    return render(request, "encyclopedia/edit.html", {
        "title": title, "content": util.get_entry(title)
    })

def random_page(request):
    choice = random.choice(util.list_entries())
    return redirect("/wiki/" + choice)