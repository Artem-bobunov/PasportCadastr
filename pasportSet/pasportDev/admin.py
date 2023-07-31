from django.contrib import admin
from import_export import resources
#from django.core.models import Building
# Register your models here.
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import PasportModel, Documents,Building

# Register your models here.
class cadastrAdmnin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display_list = ('numberpp')

# Регистрируем наш сайт в админке
admin.site.register(PasportModel,cadastrAdmnin)
admin.site.register(Documents,cadastrAdmnin)
admin.site.register(Building,cadastrAdmnin)
admin.site.site_header = "Центр Администрирования ГКО"

class BuildingModelAdmin(resources.ModelResource):

    class Meta:
        model = Building
        fields = ('urbanRualSet','municipalArea','urbanDistrict','intracityDistrict',
                        'street','numberHouse','numberCorpus','numberRootFlat')
        export_order = ('urbanRualSet','municipalArea','urbanDistrict','intracityDistrict',
                        'street','numberHouse','numberCorpus','numberRootFlat')

class PasportModelAdmin(resources.ModelResource):

    class Meta:
        model = PasportModel
        fields = ('city','numberpp','inventerNumber','earlyNumber','viewObject',
                        'purpose','nameObject','dateInitialInvent','dateLastExamination',
                  'yearCommissioning','square','residentialSquare','ownershipBefore',
                  'ownershipAfter','whoHanded','remark','dateIssueInventory','returnDate','storage')
