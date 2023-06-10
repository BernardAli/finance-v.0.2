from django.shortcuts import render
from .models import Topics, FirstAlphabet, Term


# Create your views here.


def dictionary(request):
    topics = Topics.objects.all()
    alphabet = FirstAlphabet.objects.all()
    day_term = Term.objects.all().first()
    common_terms = Term.objects.all()[:10]
    context = {
        'topics': topics,
        'alphabet': alphabet,
        'day_term': day_term,
        'common_terms': common_terms
    }
    return render(request, 'education/dictionary.html', context)


def topic_details(request, topic_slug):
    topic = Topics.objects.get(slug=topic_slug)
    terms = Term.objects.filter(topic__slug=topic_slug)
    terms_count = Term.objects.filter(topic__slug=topic_slug).count()

    context = {
        'topic': topic,
        'terms': terms,
        'terms_count': terms_count
    }
    return render(request, 'education/topic_list.html', context)


def alphabet_details(request, alpha_slug):
    alphabet = FirstAlphabet.objects.get(slug=alpha_slug)
    terms = Term.objects.filter(first_letter__slug=alpha_slug)
    terms_count = Term.objects.filter(first_letter__slug=alpha_slug).count()

    context = {
        'alphabet': alphabet,
        'terms': terms,
        'terms_count': terms_count
    }
    return render(request, 'education/alpha_list.html', context)


def term_details(request, id):
    term = Term.objects.get(id=id)

    context = {
        'term': term
    }
    return render(request, 'education/term_details.html', context)
