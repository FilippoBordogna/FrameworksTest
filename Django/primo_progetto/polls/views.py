from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

# VISTE GENERICHE

# ListView usa un template di default chiamato <app name>/<model name>_list.html
# Nel nostro caso, dovrebbe usare il template "polls/question_list"
# La variabile di contesto generata automaticamente è question_list
class IndexView(generic.ListView): # Modello ListView
    template_name = 'polls/index.html' # template specifico invece del nome di template generato automaticamente
    context_object_name = 'latest_question_list' # Sovrascrivo la variabile di contesto generata automaticamente

    def get_queryset(self): # Restituisce le ultime 5 domande NON tenendo conto di quelle schedulate in futuro
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

# DetailView usa un template chiamato <app name>/<model name>_detail.html. 
# Nel nostro caso, dovrebbe usare il template "polls/question_detail.html"
# La variabile di contesto generata automaticamente è question
class DetailView(generic.DetailView): #Modello DetailView: Si aspetta che la chiave primaria che viene passata dalla URL si chiami "pk"
    model = Question 
    template_name = 'polls/detail.html' # template specifico invece del nome di template generato automaticamente

    def get_queryset(self):
        """
        Esclude le domande che non sono ancora state pubblicate.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html' # template specifico invece del nome di template generato automaticamente

# VISTE CLASSICHE

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id) # Prendo la domanda con pk = question_id. Se non esiste Errore 404
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice']) # Prendo l'oggetto scelta corrispondente alla risposta
    except (KeyError, Choice.DoesNotExist): # Non esiste una scelta con pk = valore_form
        # Rimostro la form contenente domanda e risposte tra cui scegliere (chiamata polls/detail).
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1 # Incremento i voti
        selected_choice.save() # Salvo
        # Ritorno un HttpResponseRedirect dopo il successo di una post per prevenire il riPost conseguente al tasto indietro
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,))) # reverse(nome-view) ; args=argomenti che richiede la view