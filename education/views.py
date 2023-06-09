from django.shortcuts import render
from .models import Topics, FirstAlphabet, Term


# Create your views here.


def dictionary(request):
    topics = Topics.objects.all()
    alphabet = FirstAlphabet.objects.all()
    context = {
        'topics': topics,
        'alphabet': alphabet
    }
    return render(request, 'education/dictionary.html', context)


def topic_details(request, topic_slug):
    topic = Topics.objects.get(slug=topic_slug)
    terms = Term.objects.filter(topic__slug=topic_slug)

    context = {
        'topic': topic,
        'terms': terms
    }
    return render(request, 'education/topic_list.html', context)


def term_details(request, id):
    term = Term.objects.get(id=id)

    context = {
        'term': term
    }
    return render(request, 'education/term_details.html', context)
