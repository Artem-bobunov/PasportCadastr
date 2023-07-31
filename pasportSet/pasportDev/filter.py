from django.forms import *
from .models import *
import django_filters
from django_filters import DateFromToRangeFilter, AllValuesFilter, CharFilter, DateFilter, NumberFilter, ChoiceFilter, \
    RangeFilter, DateRangeFilter,ModelChoiceFilter
from django_filters.widgets import RangeWidget, LinkWidget

class MRFilter(django_filters.FilterSet):
    inventerNumber = CharFilter(widget=TextInput(attrs={'class': 'form-control'}), label="Инвентарный номер")
    # inputDate =  DateRangeFilter(widget=TextInput(attrs={'class': 'form-control'}),label="Дата регистрации")
    #ownershipBefore = CharFilter(widget=TextInput(attrs={'class': 'form-control'}), label="Право собственности до 01.01. 1999г.")
    #ownershipAfter = CharFilter(widget=TextInput(attrs={'class': 'form-control'}), label="Право собственности после 01.01. 1999г.")
    dateIssueInventory = DateFromToRangeFilter(widget=RangeWidget(attrs={'class': 'form-control','type': 'date'}),label="Дата возврата дел")
    returnDate = DateFromToRangeFilter(widget=RangeWidget(attrs={'class': 'form-control','type': 'date'}),label="Дата выдачи инвентарного дела")

    class Meta:
        model = PasportModel
        fields = ['inventerNumber','ownershipBefore','ownershipAfter','dateIssueInventory','returnDate']

class exportCSV(django_filters.FilterSet):
    inventerNumber = CharFilter(widget=TextInput(attrs={'class': 'form-control'}), label="Инвентарный номер")
    # inputDate =  DateRangeFilter(widget=TextInput(attrs={'class': 'form-control'}),label="Дата регистрации")
    #ownershipBefore = CharFilter(widget=TextInput(attrs={'class': 'form-control'}), label="Право собственности до 01.01. 1999г.")
    #ownershipAfter = CharFilter(widget=TextInput(attrs={'class': 'form-control'}), label="Право собственности после 01.01. 1999г.")
    dateIssueInventory = DateFromToRangeFilter(widget=RangeWidget(attrs={'class': 'form-control','type': 'date'}),label="Дата выдачи инвентарного дела")
    returnDate = DateFromToRangeFilter(widget=RangeWidget(attrs={'class': 'form-control','type': 'date'}),label="Дата возврата дел")
    dateInputPS = DateFromToRangeFilter(widget=RangeWidget(attrs={'class': 'form-control','type': 'date'}),label="Дата внесения дела")
    #urbanRualSet = ModelChoiceFilter(lookup_expr='icontains', label='Room', distinct=True)

    class Meta:
        model = PasportModel
        fields = ['dateInputPS','inventerNumber','dateIssueInventory','returnDate']