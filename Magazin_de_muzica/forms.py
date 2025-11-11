from django import forms
from .models import Categorie, Campanie_Promo
PAGINATION_CHOICES = [
    (5, '5 pe pagină (Implicit)'), 
    (10, '10 pe pagină'),
    (30, '30 pe pagină'),
    (50, '50 pe pagină'),
]
class ProductFilterForm(forms.Form):
    #lab 5 ex 6
    categorie = forms.ModelChoiceField(
        queryset=Categorie.objects.all(), 
        label='Categorie', 
        required=False,
        empty_label="Toate Categoriile" 
    )
    denumire = forms.CharField(
        max_length=200, 
        label='Căutare Denumire', 
        required=False,
        #lab 5 ex 4
        widget=forms.TextInput(attrs={'placeholder': 'Căutare parțială...'})
    )

    pret_min = forms.IntegerField(
        label='Preț Min.', 
        required=False, 
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Min'})
    )
    pret_max = forms.IntegerField(
        label='Preț Max.', 
        required=False, 
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Max'})
    )

    stoc_min = forms.FloatField(
        label='Stoc Min.', 
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Min'})
    )
    stoc_max = forms.FloatField(
        label='Stoc Max.', 
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Max'})
    )
    campanii = forms.ModelMultipleChoiceField(
        queryset=Campanie_Promo.objects.all(), 
        label='Campanii Incluse', 
        required=False,
        help_text="Filtrează produsele care fac parte din oricare dintre campaniile selectate."
    )
    data_adaugare_min = forms.DateTimeField(
        label='Adăugat după',
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    data_adaugare_max = forms.DateTimeField(
        label='Adăugat înainte',
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    are_imagine = forms.BooleanField(
        label='Doar produse cu imagine',
        required=False
    )
    
    #lab 5 ex 7 alegerea nr de produse pe pagina
    
    produse_per_pagina = forms.ChoiceField(
        choices=PAGINATION_CHOICES,
        label='Produse afișate',
        required=False,
        initial=PAGINATION_CHOICES[0][0] 
    )
    
    #lab 5 ex 5
    
    def clean(self):
        cleaned_data = super().clean()
        pret_min = cleaned_data.get('pret_min')
        pret_max = cleaned_data.get('pret_max')
        if pret_min is not None and pret_max is not None and pret_min > pret_max:
            raise forms.ValidationError('Prețul minim nu poate fi mai mare decât prețul maxim.')

        stoc_min = cleaned_data.get('stoc_min')
        stoc_max = cleaned_data.get('stoc_max')
        if stoc_min is not None and stoc_max is not None and stoc_min > stoc_max:
            raise forms.ValidationError('Stocul minim nu poate fi mai mare decât stocul maxim.')

        data_adaugare_min = cleaned_data.get('data_adaugare_min')
        data_adaugare_max = cleaned_data.get('data_adaugare_max')
        if data_adaugare_min and data_adaugare_max and data_adaugare_min > data_adaugare_max:
            raise forms.ValidationError('Data adăugării minime nu poate fi după data maximă.')

        return cleaned_data