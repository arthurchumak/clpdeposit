# -*- coding: utf-8 -*-
from math import *

from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from app.forms import DoVostredDepositForm, NakopDepositForm, RaschDepositForm, IndexDepositForm, SberegDepositForm
from app.models import Deposit, DepositType


@login_required
@user_passes_test(lambda u: u.is_superuser)
def list(request, deposit_id=None):
    if deposit_id != None:
        try:
            d = Deposit.objects.get(pk=deposit_id)
            if d:
                d.is_archive = True
                d.save()
        except:
            pass
    depositList = Deposit.objects.all().order_by('is_archive')
    return render(request, 'deposit/list.html', {
        'depositList': depositList.filter(is_archive=False),
        'depositListArch': depositList.filter(is_archive=True),
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def all(request):
    depositList = DepositType.objects.all()
    return render(request, 'deposit/all.html', {
        'depositList': depositList
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def new(request, deposit_id):
    try:
        errors = []

        depositType = DepositType.objects.get(pk=deposit_id)

        if depositType.title == 'Вклад до востребования':
            F = DoVostredDepositForm
        elif depositType.title == 'Cберегательный вклад':
            F = SberegDepositForm
        elif depositType.title == 'Накопительный вклад':
            F = NakopDepositForm
        elif depositType.title == 'Расчетный вклад':
            F = RaschDepositForm
        else:  # depositType.title == 'Индексируемый вклад':
            F = IndexDepositForm

        if request.method == 'POST':
            depositForm = F(request.POST)
            if depositForm.is_valid():
                d = depositForm.save(commit=False)
                good = True

                if depositType.title != 'Вклад до востребования' and d.percent <= d.percent_for_early_withdrawal:
                    errors.append('Процентная ставка при преждевременном снятии должна быть меньше начальной')
                    good = False
                if Deposit.objects.filter(title=d.title, is_archive=False):
                    errors.append('Вклад с таким названием уже существует')
                    good = False
                if d.duration < d.pay_period and depositType.title != 'Вклад до востребования':
                    errors.append('Период выплат не должен привышать срок хранения')
                    good = False
                if depositType.title != 'Вклад до востребования' and fmod(d.duration, d.pay_period) != 0:
                    errors.append('Период выплат должен быть кратен сроку хранения')
                    good = False
                if d.min_amount <= d.minimum_balance and (
                                depositType.title == 'Расчетный вклад' or depositType.title == 'Индексируемый вклад'):
                    errors.append('Неснижаемый остаток должен быть меньше минимальной начальной суммы')
                    good = False
                if depositType.title == 'Индексируемый вклад' and d.binding_currency == d.currency:
                    errors.append('Валюта привязки должна отличаться от основной валюты')
                    good = False
                if good:
                    if depositType.title == 'Вклад до востребования':
                        d.is_early_withdrawal = True
                        d.is_refill = True
                    elif depositType.title == 'Накопительный вклад':
                        d.is_refill = True
                    elif depositType.title == 'Расчетный вклад':
                        d.is_early_withdrawal = True
                        d.is_refill = True

                    d.depositType = depositType
                    d.save()
                    return redirect('deposit:list')
        else:
            depositForm = F()

        return render(request, 'deposit/new.html', {
            'depositForm': depositForm,
            'errors': errors,
            'ID': deposit_id,
            'depositType': depositType
        })
    except:
        return HttpResponse(status=404)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit(request, deposit_id):
    try:
        errors = []
        oldDeposit = Deposit.objects.get(pk=deposit_id)
        depositType = oldDeposit.depositType

        if depositType.title == 'Вклад до востребования':
            F = DoVostredDepositForm
        elif depositType.title == 'Cберегательный вклад':
            F = SberegDepositForm
        elif depositType.title == 'Накопительный вклад':
            F = NakopDepositForm
        elif depositType.title == 'Расчетный вклад':
            F = RaschDepositForm
        else:  # depositType.title == 'Индексируемый вклад':
            F = IndexDepositForm

        if request.method == 'POST':
            depositForm = F(request.POST)
            if depositForm.is_valid():
                d = depositForm.save(commit=False)
                good = True

                if depositType.title != 'Вклад до востребования' and d.percent <= d.percent_for_early_withdrawal:
                    errors.append('Процентная ставка при преждевременном снятии должна быть меньше начальной')
                    good = False
                if Deposit.objects.filter(title=d.title, is_archive=False).exclude(title=oldDeposit.title):
                    errors.append('Вклад с таким названием уже существует')
                    good = False
                if d.title == oldDeposit.title and Deposit.objects.filter(title=d.title, is_archive=False).exclude(
                        id=oldDeposit.id):
                    errors.append('Кто-то изменил вклад раньше вас(')
                    good = False
                if depositType.title != 'Вклад до востребования' and d.duration < d.pay_period:
                    errors.append('Период выплат не должен привышать срок хранения')
                    good = False
                if depositType.title != 'Вклад до востребования' and fmod(d.duration, d.pay_period) != 0:
                    errors.append('Период выплат должен быть кратен сроку хранения')
                    good = False
                if d.min_amount <= d.minimum_balance and (
                                depositType.title == 'Расчетный вклад' or depositType.title == 'Индексируемый вклад'):
                    errors.append('Неснижаемый остаток должен быть меньше минимальной начальной суммы')
                    good = False
                if depositType.title == 'Индексируемый вклад' and d.binding_currency == d.currency:
                    errors.append('Валюта привязки должна отличаться от основной валюты')
                    good = False
                if good:
                    if depositType.title == 'Вклад до востребования':
                        d.is_early_withdrawal = True
                        d.is_refill = True
                    elif depositType.title == 'Накопительный вклад':
                        d.is_refill = True
                    elif depositType.title == 'Расчетный вклад':
                        d.is_early_withdrawal = True
                        d.is_refill = True

                    oldDeposit.is_archive = True
                    oldDeposit.save()

                    d.depositType = depositType
                    d.save()
                    return redirect('deposit:list')
        else:
            depositForm = F(instance=oldDeposit)

        return render(request, 'deposit/edit.html', {
            'depositForm': depositForm,
            'errors': errors,
            'ID': deposit_id,
            'depositType': depositType
        })
    except:
        return HttpResponse(status=404)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def info(request, deposit_id):
    return render(request, 'deposit/info.html', {
        'deposit': Deposit.objects.get(id=deposit_id)
    })
