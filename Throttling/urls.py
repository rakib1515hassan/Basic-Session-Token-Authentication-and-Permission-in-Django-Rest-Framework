from django.urls import path
from Throttling.views import (
    Student_Throttling,
    ContentListView,
    ContentCreateView,
    ContentRetrieveView,
    ContentUpdateView,
    )


urlpatterns = [

    path('student-throt/', Student_Throttling.as_view()),

    path('student-throt-list/',    ContentListView.as_view()),
    path('student-throt-create/',  ContentCreateView.as_view()),
    path('student-throt-retrieve/<int:pk>/',ContentRetrieveView.as_view()),
    path('student-throt-update/<int:pk>/',  ContentUpdateView.as_view()),
]