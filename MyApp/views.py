from django.shortcuts import render,redirect
from django.http import HttpResponse
import pandas as pd 
from django.core.files.storage import default_storage


def index(request):
    if request.method == 'POST':
        # getting the name from home page
        name = request.POST.get('name')
        # storing name in session
        request.session['name']=name
        return render(request,'index.html',{'name':name})
    # user directly want to go to summary page
    elif request.session.get('name'):
        return render(request,'index.html',{'name':request.session.get('name')})
    # direct want to go to upload_file page
    return redirect('home')
def home(request):
    # open base url
    return render(request,'home.html')
def summary(request):
    # if file uploaded sucessfully
    if request.method=='POST' and request.FILES['fileUpload']:
        uploaded_file=request.FILES['fileUpload']
        file_path=default_storage.save(uploaded_file.name,uploaded_file)
        if uploaded_file.name.endswith('.csv'):
            df=pd.read_csv(file_path)

        elif uploaded_file.name.endswith(('.xls','.xlsx')):
            df=pd.read_excel(file_path)
        else:
            return HttpResponse("Invalid file type.",status=400)
        shape=df.shape
        summary=df.describe().to_html(classes='table table-striped')
        missing=dict(df.isnull().sum())
        duplicate=df.duplicated().sum()
        name = request.session.get('name')
        default_storage.delete(file_path)
        # in case name is missing
        if request.session.get('name')==None:
          
            return redirect('home')
        # delete name for upload another file 
        del request.session['name']
        return render(request, 'summary.html', {'name':name,'summary': summary,'duplicate':duplicate,'missing':missing,'shape':shape})
    # is case name is missing and user directly want to go url
    elif request.session.get('name')==None and request.method=='GET':
         return redirect('home')
    # in case name is filed and user directly want to go summary page
    else:
         return redirect('upload_file')