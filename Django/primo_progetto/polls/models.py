from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin

# Classe Domanda: TestoDomanda ; DataPubblicazione
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    # Restituisce la stringa della domanda anzichè l'oggetto
    def __str__(self): 
        return self.question_text
    
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    ) # Dichiaro la visualizzazione della funzione was_published_recently
    
    def was_published_recently(self):
        '''
        Restituisce True se la domanda è stata pubblicata meno di un giorno fa ; False altrimenti
        '''
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now # Controllo che la data di pubblicazione sia nelle precedenti 24h e NON nel futuro

# Classe Scelta : IdDomanda ; TestoScelta ; NumeroVoti
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
     # Restituisce la stringa della risposta anzichè l'oggetto
    def __str__(self):
        return self.choice_text