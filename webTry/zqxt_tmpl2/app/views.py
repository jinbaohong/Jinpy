# -*- coding: utf-8 -*-
# @Date    : 2015-10-29 21:13:35
# @Author  : Weizhong Tu (mail@tuweizhong.com)
# @Link    : http://www.tuweizhong.com
# 自强学堂 http://www.ziqiangxuetang.com

from django.shortcuts import render


def home(request):
    TutorialList = ["HTML\n", "CSS\n", "jQuery\n", "Python", "Django"]
    infodict = {'site': 'Hogwaltz', 'content': 'A bunch of magic course'}
    return render(request, 'home.html', {'TutorialList1': TutorialList, 'info_dict': infodict})
