from .models import Videos
from django.forms import ModelForm
from django import forms

# declaring the ModelForm
class EditVideoForm(forms.ModelForm):
    
    class Meta:
        # the Model from which the form will inherit from
        model = Videos
        # the fields we want from the Model
        fields = '__all__'
        # styling the form with bootstrap classes
        widgets = {
             'video_name': forms.TextInput(attrs={'class': 'form-control'}),
             'video_path': forms.TextInput(attrs={'class': 'form-control'}),             
        }