from django.urls import path
from .views import dictionary, topic_details, term_details


urlpatterns = [
    path('dictionary/', dictionary, name="dictionary"),
    path('topic_details/<topic_slug>', topic_details, name='topic_details'),
    path('term_details/<int:id>', term_details, name='term_details'),
]