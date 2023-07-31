from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import PasportModel,Building,Documents
from .forms import PasportForms,BuildingForms,DocumentsForm
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from .filter import MRFilter,exportCSV
from django.contrib import admin
from django.db.models import Q
import time
import csv
import base64
from base64 import b64encode
from datetime import datetime
import time
import datetime
from .logger import LoggerPasport
import binascii
from io import StringIO

BLOG_POSTS_PER_PAGE = 15

def exportcsv(request):
    obj = PasportModel.objects.all()
    # id_build = Building.objects.latest('id').id
    # print(id_build)
    csv_filter = exportCSV(request.GET, queryset=obj)
    obj = csv_filter.qs
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="file.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Администратор', 'city',
                     'Инвентарный номер', 'Ранее присвоенный инвентарный номер','Городское/ сельское поселение','Муниципальный район','Городской округ',
                     'Внутригородской район','улица, пер. и т.д.','номер дома','номер корпуса','номер комнаты, квартиры', 'Вид объекта',
                     'Наименование объекта', 'Дата первичного формирования инвентарного дела', 'Дата последнего обследования',
                     'Год ввода в эксплуатацию', 'Общая площадь', 'жилая площадь', 'Право собственности до 01.01. 1999г.',
                     'Право собственности после  01.01. 1999г', 'Кем передан/ изготовлен',
                     'Примечание', 'Дата выдачи инвентарного дела', 'Дата возврата дела', 'Место хранения документа'])

    for e in obj.values_list('id', 'userbti', 'city', 
                             'inventerNumber', 'earlyNumber','city__urbanRualSet','city__municipalArea','city__urbanDistrict',
                             'city__intracityDistrict','city__street','city__numberHouse','city__numberCorpus','city__numberRootFlat',
                             'viewObject', 'nameObject', 'dateInitialInvent', 'dateLastExamination',
                             'yearCommissioning', 'square', 'residentialSquare', 'ownershipBefore',
                             'ownershipAfter', 'whoHanded', 'remark', 'dateIssueInventory', 'returnDate', 'storage'
                             ):
        writer.writerow(e)
    return response

def home(request):
    start_time = time.time()
    counts = PasportModel.objects.count()
    obj = PasportModel.objects.all().order_by('-id')
    expcsv = exportCSV(request.GET, queryset=obj) 

    #myFilter = MRFilter(request.GET, queryset=obj)
    obj = expcsv.qs
    coun =obj.count()
    if request.method == 'POST':
            if request.POST.get('save_home'):
                
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="report.csv"'
                writer = csv.writer(response)
                writer.writerow(['Инвентарный номер', 'Городской округ',
                                 'улица, пер. и т.д.', 'номер дома',
                                 'номер комнаты, квартиры','Наименование объекта',
                                 'Право собственности до 01.01. 1999г.',
                                 'Право собственности после  01.01. 1999г',
                                 'Дата выдачи инвентарного дела', 'Дата возврата дела',
                                 ])

                for e in obj.values_list('inventerNumber', 'city__urbanDistrict',
                                         'city__street', 'city__numberHouse',
                                         'city__numberRootFlat',
                                         'nameObject', 'ownershipBefore',
                                         'ownershipAfter',  'dateIssueInventory', 'returnDate',
                                         ):
                    writer.writerow(e)
                return response
    paginator = Paginator(obj, BLOG_POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    try:
        pages = paginator.page(page_number)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return_time = time.time() - start_time
    
    
    context ={'form':obj,'filter':expcsv,'page':pages,'counts':counts,'coun':coun,'t':return_time}
    return render(request,"list.html",context)

def create(request):

    if request.method == "POST":
        pasport_form = PasportForms(request.POST or None)
        build_form = BuildingForms(request.POST or None)
        docform = DocumentsForm(request.POST or None, request.FILES)#, request.FILES
        files = request.FILES.getlist('file')
        current_date = str(datetime.datetime.now().date())
        date2 = datetime.datetime.strptime(current_date,'%Y-%m-%d')
        print(files)
        if pasport_form.is_valid() or build_form.is_valid() or docform.is_valid():
            try:
                build_form.save()
                instance=pasport_form.save()
                instance.city = Building.objects.order_by('id').last()
                instance.dateInputPS=date2
                instance.userbti = request.user
                instance.save()

                id_doc = PasportModel.objects.order_by('id').last()

                for i in files:
                    docform = Documents(file_name=i, file_binary=i.file.read(), file_doc=id_doc)
                    docform.save()
                """
                #Физическое сохранение файлов
                for f in files:
                    docform = Documents(file = f,file_binary =f,file_doc =id_doc)
                    docform.save()
                    print("Выполнилось")
                """
                return redirect('/')
            except:
                print("Не удалось сохранить")
    else:
        pasport_form = PasportForms()
        build_form = BuildingForms()
        docform = DocumentsForm()
    return render(request, 'create.html', {'form': pasport_form,'build_form':build_form,'docform':docform})

@login_required
def view_image_binary(request,id):

    arr =[]
    fn = None
    fn_id = None
    if request.method == 'GET':
        try:
            df = Documents.objects.filter(file_doc=id)
            for i in df:
                arr.append(base64.b64encode(i.file_binary).decode())
            fn = PasportModel.objects.get(id=id).inventerNumber
        except:
            print("Не удалось просмотреть детали")
    return render(request, "detail_image.html",  context ={'docform':arr,'fn':fn,})

def detail(request, id):
#SELECT file FROM public."pasportDev_documents", public."pasportDev_pasportmodel" where id_pasport  =  public."pasportDev_pasportmodel".id;
    #context = {}
    buildform = None
    details =None
    if request.method == "GET":
        try:
            details = PasportModel.objects.get(pk=id)
            buildform = Building.objects.get(pk=id)
            #df = Documents.objects.filter(file_doc=id)
        except:
            print("Не удалось просмотреть детали")
    #context['buildform'] = buildform
    return render(request, "detail.html",  context ={'details':details,'buildform':buildform})

@login_required
def update (request,id):

    pasport = PasportModel.objects.get(id=id)
    dips = pasport.dateInputPS
    doc = Documents.objects.filter(file_doc=id)
    build = Building.objects.get(id=id)
    form1 = PasportForms(instance=pasport)
    form2 = BuildingForms(instance=build)
    form3 = DocumentsForm()
    if request.method == 'POST':
        form1 = PasportForms(request.POST or None,instance=pasport)
        form2 = BuildingForms(request.POST or None, instance=build)
        form3 = DocumentsForm(request.POST or None ,request.FILES or None)
        files = request.FILES.getlist('file',None)
        get_file_delete = request.POST.getlist('check',None)
        if form1.is_valid() or form2.is_valid() or form3.is_valid() :
                try:
                    instance = form1.save()
                    instance.city = Building.objects.get(id=id)
                    instance.userbti = request.user
                    instance.dateInputPS = dips
                    instance.save()
                    form2.save()
                    for f in files:
                        form3 = Documents(file_name=f,file_binary = f.file.read(), file_doc=pasport)
                        form3.save()
                    for i in get_file_delete:
                        file_delete = Documents.objects.filter(file_name=i)
                        file_delete.delete()
                    x = LoggerPasport(request.user, instance.inventerNumber)
                    x.update_record()
                    return HttpResponseRedirect('/detail/'+str(id))
                except Exception as e:
                    print(e)
        else:
            form1 = PasportForms()
            form2 = BuildingForms()
            form3 = DocumentsForm()

    return render(request, 'update.html', {'form': form1,'form2': form2,'form3': form3,'pasport':pasport,'doc':doc})


@login_required
def delete (request, id):
    build = Building.objects.get(id=id)
    obj = PasportModel.objects.get(id=id)
    doc = Documents.objects.filter(file_doc = id)
    if request.method == "POST":
        try:
            build.delete()
            obj.delete()
            for i in doc:
                del_doc = i.file
                del_doc.delete()
                #print("Удалили: ", i.file.name)
            x = LoggerPasport(request.user, obj.inventerNumber)
            x.delete_record()
            return HttpResponseRedirect('/')
        except:
            print("Не удалось удалить запись")
    context = {'obj':obj}
    return render(request, "delete.html", context)

def searchList(request):
    start_time = time.time()
    query_dict = request.GET
    query  = query_dict.get("q")
    list_object = None
    if query is not None:
        list_object = PasportModel.objects.filter(Q(inventerNumber__icontains=query) |
                                                Q(ownershipBefore__icontains = query) |
                                                Q(ownershipAfter__icontains=query) |
                                                Q(city__numberHouse__icontains=query)|
                                                Q(city__urbanRualSet__icontains=query)|
                                                Q(city__municipalArea__icontains=query)|
                                                Q(city__urbanDistrict__icontains=query)|
                                                Q(city__intracityDistrict__icontains=query)|
                                                Q(nameObject__icontains=query)|
                                                Q(city__street__icontains=query))
    print(list_object.values())
    if request.method == 'POST':
            if request.POST.get('save_home'):
                
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="report.csv"'
                writer = csv.writer(response)
                writer.writerow(['Инвентарный номер', 'Городской округ',
                                 'улица, пер. и т.д.', 'номер дома',
                                 'номер комнаты, квартиры','Наименование объекта',
                                 'Право собственности до 01.01. 1999г.',
                                 'Право собственности после  01.01. 1999г',
                                 'Дата выдачи инвентарного дела', 'Дата возврата дела',
                                 ])

                for e in list_object.values_list('inventerNumber', 'city__urbanDistrict',
                                         'city__street', 'city__numberHouse',
                                         'city__numberRootFlat',
                                         'nameObject', 'ownershipBefore',
                                         'ownershipAfter',  'dateIssueInventory', 'returnDate',
                                         ):
                    writer.writerow(e)
                return response
    paginator = Paginator(list_object, BLOG_POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    try:
        pages = paginator.page(page_number)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    count_oblect = list_object.count()
    #Выгрузка данных по запросу
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=students.csv'
    writer = csv.writer(response)
    writer.writerow(['id', 'userbti', 'city',
                     'inventerNumber', 'earlyNumber', 'viewObject',
                     'nameObject','dateInitialInvent', 'dateLastExamination',
                     'yearCommissioning','square','residentialSquare','ownershipBefore',
                     'ownershipAfter','whoHanded','remark','dateIssueInventory','returnDate','storage'
                     ])
    studs = list_object.values_list('id', 'userbti', 'city', 
                     'inventerNumber', 'earlyNumber', 'viewObject'
                     ,'nameObject','dateInitialInvent', 'dateLastExamination',
                     'yearCommissioning','square','residentialSquare','ownershipBefore',
                     'ownershipAfter','whoHanded','remark','dateIssueInventory','returnDate','storage')
    for std in studs:
        writer.writerow(std)
    return_time=time.time() - start_time
    #data = download_csv(admin.ModelAdmin, request, PasportModel.objects.all())
    context = {"count_oblect":count_oblect,'list_object':list_object,'return_time':return_time,'pages':pages}
    return render(request,"list.html",context=context)

