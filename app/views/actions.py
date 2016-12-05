# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.models import Bill, Contract


@login_required
def bill(request):
    try:
        bill_actions = Bill.objects.get(id=request.POST['num'], client=request.user).get_actions().order_by('-id')
        return render(request, 'bill/bill_operations.html', {'bills': bill_actions})
    except:
        return render(request, 'bill/bill_operations.html', {'bills': {}})

@login_required
def contract(request):
    try:
        contracts = Contract.objects.get(id=request.POST['num'], bill__client=request.user).get_actions().order_by(
            '-id')
        return render(request, 'actions/contract_operations.html', {'contracts': contracts})
    except:
        return render(request, 'actions/contract_operations.html', {'contracts': {}})
