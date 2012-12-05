from django import forms

from .models import ImageFile



class ImageFileForm(forms.ModelForm):

    class Meta:
        model = ImageFile

    def clean_file_id(self):
        """
        We delegate field's validation to 'file' field.
        """
        return self.cleaned_data.get('file') or u''
