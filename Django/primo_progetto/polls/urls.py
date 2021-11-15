from django.urls import path

from . import views

# CHIAMATE A DISPOSIZIONE
app_name = 'polls' # Specifico il namespace in modo che altre app non creino conflitto
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), # ListView
    path('<int:pk>/', views.DetailView.as_view(), name='detail'), # DetailView: necessita del parametro pk
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'), # DetailView: necessita del parametro pk 
    path('<int:question_id>/vote/', views.vote, name='vote'), # NormalView
]