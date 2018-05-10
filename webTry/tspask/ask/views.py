# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
 
# 引入我们创建的表单类
# from .forms import tryForm
from pymongo import MongoClient
from django import forms
from django.forms.widgets import CheckboxSelectMultiple

uri = 'mongodb://172.20.23.138:27017'
client = MongoClient(uri)
db = client['ask']
collect = db['ask_list']

class tryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(tryForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False 
    choice_batch = (('台北','台北'),('台中','台中'),('高雄','高雄'))
    batch = forms.ChoiceField(label='場次',choices=choice_batch)
    companyName = forms.CharField(label='公司名稱')
    contactPerson = forms.CharField(label='聯絡人')
    phone = forms.CharField(label='電話')
    email = forms.EmailField(label='電子信箱')
    choice_export = (('None','None'), ('yes', 'yes'), ('no', 'no'),)
    isExport = forms.ChoiceField(label='是否為出口商', choices=choice_export)
    choice_planToExhibit = (('None','None'), ('yes', 'yes'), ('no', 'no'))
    planToExhibit = forms.ChoiceField(label='出國參展之計畫', choices=choice_planToExhibit)
    planToExhibit_year = forms.CharField(label='預計__年內')
    planToExhibit_where = forms.CharField(label='想去__')
    productToExport = forms.CharField(label='目標出口產品')
    HScode = forms.CharField(label='海關稅則編碼(HS code)')
    marketToExport = forms.CharField(label='目標拓銷市場')
    choice_reasonToExhibit = (('該展的前瞻性','該展的前瞻性'),
                              ('去該展要花多少錢','去該展要花多少錢'),
                              ('展覽日期','展覽日期'),
                              ('該展有沒有補助','該展有沒有補助'),
                              ('該展產業是否與公司本次拓銷產品相符','該展產業是否與公司本次拓銷產品相符'),
                              ('競爭對手或對手國參加與否','競爭對手或對手國參加與否'),
                              ('其他','其他'))
    firstReason = forms.MultipleChoiceField(label='影響去哪國參展的最重要因素', widget=CheckboxSelectMultiple(), choices=choice_reasonToExhibit)
    firstReasonOther = forms.CharField(label='請說明')
    secondReason = forms.MultipleChoiceField(label='影響去哪國參展的最次要因素', widget=CheckboxSelectMultiple(), choices=choice_reasonToExhibit)
    secondReasonOther = forms.CharField(label='請說明')
    choice_helpYou = (('None','None'), ('yes', 'yes'), ('no', 'no'))
    isHelpYou = forms.ChoiceField(label='本平台資訊有幫助？', choices=choice_helpYou)
    isHelpYou_reason = forms.CharField(label='原因')
    choice_rec = (('None','None'), ('yes', 'yes'), ('no', 'no'))
    recToOther = forms.ChoiceField(label='願意推薦平台給其他廠商？', choices=choice_rec)
    choice_recieve = (('None','None'), ('yes', 'yes'), ('no', 'no'))
    recieveInfo = forms.ChoiceField(label='願意收到平台相關資訊？', choices=choice_recieve)
    choice_helpUs = (('None','None'), ('yes', 'yes'), ('no', 'no'))
    helpUs = forms.ChoiceField(label='願意協助平台優化？', choices=choice_helpUs)
    # say = forms.CharField(
    #     max_length=2000,
    #     widget=forms.Textarea(),
    #     help_text='Write here your message!'
    # )

def index(request):
    if request.method == 'POST':# 当提交表单时
     
        form = tryForm(request.POST) # form 包含提交的数据
         
        if form.is_valid():# 如果提交的数据合法
            companyName = form.cleaned_data['companyName']
            contactPerson = form.cleaned_data['contactPerson']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            isExport = form.cleaned_data['isExport']
            firstReason = form.cleaned_data['firstReason']

            collect.insert_one(form.cleaned_data)
            return render(request,
                        'index.html',
                        {'form': form,
                         'email': email,
                         'companyName': companyName,
                         'isExport': isExport,
                         'phone': phone,
                         'firstReason': firstReason})
    else:# 当正常访问时
        form = tryForm()
    return render(request, 'index.html', {'form': form})
