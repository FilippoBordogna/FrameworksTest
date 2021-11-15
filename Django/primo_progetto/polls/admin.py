from django.contrib import admin

from .models import Question, Choice

class ChoiceInline(admin.TabularInline): # Visualizzazione tabulare
    model = Choice # Modello
    extra = 3 # Numero di 'slot' di default (puoi aggiungerne e toglierne dall'interfaccia grafica)

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}), # Area 1: Testo della domanda (il primo campo è il titolo)
        ('Date information', {'fields': ['pub_date']}), # Area 2: Data di pubblicazione
    ] # Dichiaro l'ordine di visualizzazione dei campi quando modifico/aggiungo una domanda
    inlines = [ChoiceInline] # Aggiungo il modulo ChoiceInline dichiarato sopra
    
    list_display = ('question_text', 'pub_date', 'was_published_recently') # Dichiaro l'ordine di visualizzazione dei campi nella pagina delle domande
    list_filter = ['pub_date'] # Aggiungo un filtro per data di pubblicazione (tendina a destra)
    search_fields = ['question_text'] # Aggiungo una casella di ricerca in base al testo della domanda
    
admin.site.register(Question, QuestionAdmin) # Aggiungo all'interfaccia Question seguendo il modello dichiarato