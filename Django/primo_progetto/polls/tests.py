import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        '''
        was_published_recently() 
        dovrebbe ritornare False per domande la cui pub_date è nel futuro.
        '''
        
        time = timezone.now() + datetime.timedelta(days=30) # Timezone futuro (fra 30 giorni)
        future_question = Question(pub_date=time) # Creo la domanda (nel futuro)
        self.assertIs(future_question.was_published_recently(), False) # Testo la funzione was_published_recently() che dovrebbe restituire False
        
    def test_was_published_recently_with_old_question(self):
        '''
        was_published_recently() 
        dovrebbe ritornare False per le domande la cui pub_date è più vecchia di un giorno.
        '''
        
        time = timezone.now() - datetime.timedelta(days=1, seconds=1) # Timezone ieri -1 secondo
        old_question = Question(pub_date=time) # Creo la domanda
        self.assertIs(old_question.was_published_recently(), False) # Testo la funzione was_published_recently() che dovrebbe restituire False

    def test_was_published_recently_with_recent_question(self):
        '''
        was_published_recently() 
        dovrebbe ritornare True per le domande la cui pub_date è entro ieri
        '''
        
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59) # Timezone ieri +1 secondo
        recent_question = Question(pub_date=time) # Creo la domanda
        self.assertIs(recent_question.was_published_recently(), True) # Testo la funzione was_published_recently() che dovrebbe restituire True

# NOTA: La funzione è fuori dalla classe        
def create_question(question_text, days):
    """
    Crea una domanda con testo uguale a quello del parametro question_text
    e pubblicato con scostamento pari al valore del parametro days (<0 -> pubblicato nel passato ; >0 -> pubblicato nel futuro)
    """
    time = timezone.now() + datetime.timedelta(days=days) # Creo il timezione partendo da quello di oggi e scostando per il numero di giorni
    return Question.objects.create(question_text=question_text, pub_date=time) # Creo la domanda
  
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        Se non esistono domande dovrei mostrare un messaggio appropriato
        """
        
        response = self.client.get(reverse('polls:index')) # Prendo la risposta alla chiamata alla view index
        self.assertEqual(response.status_code, 200) # Il codice di risposta dovrebbe essere 200 (TUTTO OK)
        self.assertContains(response, "No polls are available.") # La risposta dovrebbe essere "No polls are available"
        self.assertQuerysetEqual(response.context['latest_question_list'], []) # La lista delle ultime domande dovrebbe essere vuota

    def test_past_question(self):
        """
        Le domande con pub_date passata dovrebbero essere mostrate nella pagina di indice
        """
        
        question = create_question(question_text="Past question.", days=-30) # Creo una domanda con data di pubblicazione passata
        response = self.client.get(reverse('polls:index')) # Prendo la risposta alla chiamata alla view index
        self.assertQuerysetEqual(
                                    response.context['latest_question_list'],
                                    [question],
                                ) # La lista delle ultime domande dovrebbe contenere solo la domanda inserita 

    def test_future_question(self):
        """
        Le domande con pub_date futura NON dovrebbero essere mostrate nella pagina di indice
        """
        
        create_question(question_text="Future question.", days=30) # Creo una domanda con data di pubblicazione futura
        response = self.client.get(reverse('polls:index')) # Prendo la risposta alla chiamata alla view index
        self.assertContains(response, "No polls are available.") # La risposta dovrebbe essere "No polls are available"
        self.assertQuerysetEqual(response.context['latest_question_list'], []) # La lista delle ultime domande dovrebbe essere vuota

    def test_future_question_and_past_question(self):
        """
        Se esistono sia domande pubblicate nel passato che nel futuro,
        solo le domande pubblicate nel passato dovrebbero essere mostrate
        """
        
        question = create_question(question_text="Past question.", days=-30) # Creo una domanda con data di pubblicazione passata
        create_question(question_text="Future question.", days=30) # Creo una domanda con data di pubblicazione futura
        response = self.client.get(reverse('polls:index')) # Prendo la risposta alla chiamata alla view index
        self.assertQuerysetEqual(
                                    response.context['latest_question_list'],
                                    [question],
                                ) # La lista delle ultime domande dovrebbe contenere solo la domanda inserita con data di pubblicazione nel passato

    def test_two_past_questions(self):
        """
        La pagina index dovrebbe mostrare più domande
        """
        
        question1 = create_question(question_text="Past question 1.", days=-30) # Creo una domanda con data di pubblicazione passata (1) 
        question2 = create_question(question_text="Past question 2.", days=-5) # Creo una domanda con data di pubblicazione passata (2)
        response = self.client.get(reverse('polls:index')) # Prendo la risposta alla chiamata alla view index
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        ) # La lista delle ultime domande dovrebbe contenere tutte le domande essendo la loro data di pubblicazione nel passato
        
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        La chiamata alla vista dettaglio di una domanda con pub_date nel futuro
        dovrebbe restituire un codice 404 Not Found
        """
        
        future_question = create_question(question_text='Future question.', days=5) # Creo una domanda con data di pubblicazione futura
        url = reverse('polls:detail', args=(future_question.id,)) # Preparo l'URL della chiamata alla vista view della domanda (futura)
        response = self.client.get(url) # Prendo la risposta alla chiamata alla view detail di cui ho preparato l'URL sopra
        self.assertEqual(response.status_code, 404) # Lo stato della risposta dovrebbe essere 404

    def test_past_question(self):
        """
        La chiamata alla vista dettaglio di una domanda con pub_date nel passato
        dovrebbe mostrare il testo della domanda
        """
        past_question = create_question(question_text='Past Question.', days=-5) # Creo una domanda con data di pubblicazione passata
        url = reverse('polls:detail', args=(past_question.id,)) # Preparo l'URL della chiamata alla vista view della domanda (passata)
        response = self.client.get(url) # Prendo la risposta alla chiamata alla view detail di cui ho preparato l'URL sopra
        self.assertContains(response, past_question.question_text) # La risposta dovrebbe contenere il testo della domanda