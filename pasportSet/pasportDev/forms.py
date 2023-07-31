from django.contrib.auth.forms import AuthenticationForm
from django.forms import *
from django import forms
from django.forms import CharField
from django.forms.models import inlineformset_factory
from .models import PasportModel, Building, Documents


class PasportForms(ModelForm):
    class Meta:
        model = PasportModel
        fields = "__all__"
        widgets ={
            'inventerNumber': TextInput(attrs={'class': 'form-control','style':'width: 300px'}),
            'earlyNumber': TextInput(attrs={'class': 'form-control','style':'width: 300px'}),
            'viewObject': Select(attrs={'class': 'form-control','style':'width: 300px'}),
            'purpose': TextInput(attrs={'class': 'form-control','style':'width: 300px'}),
            'nameObject': TextInput(attrs={'class': 'form-control','style':'width: 300px'}),
            'dateInitialInvent': TextInput(attrs={'class': 'form-control','type': 'date','format':'%d.%m.%Y','style':'width: 300px'}),
            'dateLastExamination': TextInput(attrs={'class': 'form-control','type': 'date','format':'%d.%m.%Y','style':'width: 300px'}),
            'yearCommissioning': TextInput(attrs={'class': 'form-control','style':'width: 300px'}),
            'square': TextInput(attrs={'class': 'form-control','style':'width: 300px'}),
            'residentialSquare': TextInput(attrs={'class': 'form-control','style':'width: 300px'}),
            'ownershipBefore': TextInput(attrs={'class': 'form-control'}),
            'ownershipAfter': TextInput(attrs={'class': 'form-control'}),
            'whoHanded': TextInput(attrs={'class': 'form-control','style':'width: 655px'}),
            'digitization': TextInput(attrs={'class': 'form-control','style':'width: 300px'}),
            'remark': TextInput(attrs={'class': 'form-control','style':'width: 655px'}),
            'dateIssueInventory': TextInput(attrs={'class': 'form-control','type': 'date','format':'%d.%m.%Y','style':'width: 300px'}),
            'returnDate': TextInput(attrs={'class': 'form-control','type': 'date','format':'%d.%m.%Y','style':'width: 300px'}),
            'storage': TextInput(attrs={'class': 'form-control','style':'width: 325px'}),



        }

class BuildingForms(ModelForm):
    class Meta:
        model = Building
        fields = "__all__"
        widgets ={
            'urbanRualSet': TextInput(attrs={'class': 'form-control','style':'width: 300px'}),
            'municipalArea': TextInput(attrs={'class': 'form-control','style':'width: 300px'}),
            'urbanDistrict': TextInput(attrs={'class': 'form-control','style':'width: 300px'}),
            'intracityDistrict': TextInput(attrs={'class': 'form-control','style':'width: 300px'}),
            'street': TextInput(attrs={'class': 'form-control','style':'width: 300px'}),
            'numberHouse': TextInput(attrs={'class': 'form-control','style':'width: 300px'}),
            'numberCorpus': TextInput(attrs={'class': 'form-control','style':'width: 300px'}),
            'numberRootFlat': TextInput(attrs={'class': 'form-control','style':'width: 300px'}),
        }
        #
class DocumentsForm(ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,'name':'file'}),required=False)
    class Meta:
        model = Documents
        fields = ['file','file_binary','file_doc']


