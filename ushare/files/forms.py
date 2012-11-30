from django import forms

from .models import ImageFile



class ImageFileForm(forms.ModelForm):

    class Meta:
        model = ImageFile
