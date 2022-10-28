from django.shortcuts import render
from django import forms
import random
from markdown2 import Markdown 
markdowner = Markdown()

from . import util

class Search(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class':'search','placeholder': 'Search'}))

class Post(forms.Form):
    title = forms.CharField(label="Title")
    text_area = forms.CharField(widget=forms.Textarea())

class Edit(forms.Form):
    text_area = forms.CharField(widget=forms.Textarea())

def index(request):
    entries = util.list_entries()
    searched = []

    if request.method == "POST":

        #take in data submitted and save it as a form
        form = Search(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            for i in entries:
                if search in entries:
                    page = util.get_entry(search)
                    page_html = markdowner.convert(page)
                    
                    return render(request, "encyclopedia/wiki.html",{
                        "page": page_html,
                        "title": search,
                        "form": Search()
                    })
                if search.lower() in i.lower():
                    searched.append(i)
                    
            return render(request,"encyclopedia/search.html", {
                    "searched": searched,
                    "form": Search()    
                    })

        else:
            return render(request,"encyclopedia/index.html",{
                "form": form
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": Search()
        })

def wiki(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_html = markdowner.convert(page)
    
        return render(request, "encyclopedia/wiki.html",{
            "form": Search(),
            "page": page_html,
            "title": title,
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "This page was not found"})

def create(request):

    if request.method == "POST":
        form = Post(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text_area = form.cleaned_data["text_area"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html",{
                    "message": "Page already exists"
                })
            else:
                util.save_entry(title, text_area)
                page = util.get_entry(title)
                page_html = markdowner.convert(page)
                return render(request, "encyclopedia/wiki.html", {
                    "form": Search(),
                    "page": page_html,
                    "title": title
                })
    else: 
        return render(request, "encyclopedia/create.html", {
            "form": Search(),
            "post": Post()
        })

def edit(request, title):
    
    
    if request.method == "POST":
        form = Edit(request.POST or None) 
        if form.is_valid():
   
            text_area = form.cleaned_data["text_area"]
            util.save_entry(title, text_area)
            page = util.get_entry(title)
            page_html = markdowner.convert(page)
            return render(request,"encyclopedia/wiki.html",{
                "form": Search(),
                "title": title,
                "page": page_html
            })

    else:
        page = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "form": Search(),
            "edit": Edit(initial={"text_area": page})
        })

def random_page(request):
    
    if request.method == "GET":
        entries = util.list_entries()
        num = random.randint(0, len(entries)-1)
        ran_page = entries[num]
        page = util.get_entry(ran_page)
        page_html = markdowner.convert(page)
    return render(request, "encyclopedia/wiki.html",{
            "form": Search(),
            "page": page_html,
            "title": ran_page,
        })