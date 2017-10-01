from django.contrib.auth.models import User
from dal_select2 import widgets as dalWidgets
from .models import *
import django.forms as forms
from django.forms import widgets as djangoWidgets
from django.shortcuts import render

import operator
from functools import reduce
from django.db.models import Q

# Widjets
class SlotsWidget(forms.CheckboxSelectMultiple):
    template_name = "wazou"

    def get_context(self, name, value, attrs):
        context = super(SlotsWidget,self).get_context(name,value,attrs)
        for w in context['widget']['opgroups']:
            w[1]['template_name']='va mourrir'
        return context

# Forms
class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class EditActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name','slots','tags','description','minimum','maximum']
        widgets = {
            #'slots': forms.CheckboxSelectMultiple(),
            'tags': dalWidgets.ModelSelect2Multiple(url='autocomplete-tags'),
            'description': forms.Textarea
        }

    def simple_cleaned_data(self):
        d = self.cleaned_data
        d.pop('slots')
        d.pop('tags')
        return d

class SearchActivity(forms.Form):
    includeTags = forms.ModelMultipleChoiceField(label="Include", required = False, queryset=Tag.objects.all(), widget = dalWidgets.ModelSelect2Multiple(url='autocomplete-tags'))
    excludeTags = forms.ModelMultipleChoiceField(label="Exclure", required = False, queryset=Tag.objects.all(), widget = dalWidgets.ModelSelect2Multiple(url='autocomplete-tags'))
    keywords = forms.CharField(label='Mots clées', required = False, max_length=128)
    slots = forms.ModelMultipleChoiceField(label="Crénaux horaires", required = False, widget=SlotsWidget, queryset=Slot.objects.all())

    def is_valid(self):
        valid = super(SearchActivity,self).is_valid()
        
        if not valid:
            return valid

        bothTags = self.cleaned_data['includeTags'] & self.cleaned_data['excludeTags']
        if len(bothTags)>0:
            self._errors['tags_incoherents'] = "Andouille, il y a le même tag and inclure et exclure"
            return False

        return True

    def filteredActivities(self):
        a = Activity.objects.filter(name__contains=self.cleaned_data['keywords'])

        try:
            allSlots = reduce(operator.or_, (Q(slots=x) for x in self.cleaned_data['slots']))
            a = a.filter(allSlots)
        except:
            pass
        try:
            allInclude = reduce(operator.and_, (Q(tags=x) for x in self.cleaned_data['includeTags']))
            a = a.filter(allInclude)
        except:
            pass

        try:
            allExclude = reduce(operator.or_, (Q(tags=x) for x in self.cleaned_data['excludeTags']))
            a = a.exclude(allExclude)
        except:
            pass
        return a