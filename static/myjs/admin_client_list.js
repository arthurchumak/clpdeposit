$(document).ready(function () {
    getcurrencies();

    $('#myModalInfo').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        modal_event('', this, event);
        $('#myModalInfo').find('#userinfo').empty();
        $.get('/client/info/', {'user_id': Number(button.data('contentid'))}, function (data) {
            $('#myModalInfo').find('#userinfo').html(data)
        });
    });
    $('#myModalUserBills').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        modal_event('', this, event);
        $('#myModalUserBills').find('#userinfo').empty();
        $.get('/bill/userbillinfo/', {'user_id': Number(button.data('contentid'))}, function (data) {
            $('#myModalUserBills').find('#userinfo').html(data)
        });
    });

    $('#myModalNewBill').on('show.bs.modal', function (event) {
        modal_event('#addbillForm', this, event)
    });
    $('#myModalMessage').on('show.bs.modal', function (event) {
        modal_event('#messageForm', this, event)
    });
    $('#myModalFill').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        modal_event('#addonbillForm', this, event);
        $('#billfillselecttocard').empty();
        $.get('/bill/getuserbills/', {'num': Number(button.data('contentid'))}, function (data) {
            bills = data['bills'];
            for (i in bills)
                $('#billfillselecttocard').append('<option selected value=' + bills[i] + '>Счёт номер ' + bills[i] + '</option>')
        });
    });

    //==================================================================

    $('#myModalFill').submit(function (event) {
        postman('#addonbillForm', '#myModalFill', '/bill/addonbill/', event)
    });

    $('#myModalNewBill').submit(function (event) {
        postman('#addbillForm', '#myModalNewBill', '/bill/addbill/', event)
    });
    $('#myModalMessage').submit(function (event) {
        postman('#messageForm', '#myModalMessage', '/message/send/', event)
    });

    var inProgress = false;
    var loadcount = 15;

    $("#search_full").keyup(function (eventObject) {
        var search_full = $("#search_full").val();
        if ((eventObject.which != 13 && search_full != '') || inProgress == true)
            return false;
        loadcount = 15;
        $.get('/client/partiallistsearch/', {
            'full': search_full, 'loadcount': 0
        }, function (data) {
            $('#searchresult').empty();
            $('#searchresult').append(data)
        });
        return false;
    });

    $('body').on('click', '#getBillActions', function (event) {
        $.post('/actions/bill/', {'num': $(this).data('billid')}, function (data) {
            $('body').find('#_operations').html(data);
            $('body').find("#collapseThree").collapse('show');
        });
    });

    $('body').on('click', '#getContractActions', function (event) {
        $.post('/actions/contract/', {'num': $(this).data('billid')}, function (data) {
            $('body').find('#_operations').html(data);
            $('body').find("#collapseThree").collapse('show');
        });
    });


    $('#loadnextclient').click(function () {
        var search_full = $("#search_full").val();
        if (inProgress == true)
            return false;
        if (search_full != '') {
            $.ajax({
                url: '/client/partiallistsearch/', method: 'GET',
                data: {'loadcount': loadcount, 'full': search_full},
                beforeSend: function () {
                    inProgress = true;
                    $('#loadnextclient').text('Загрузка')
                }
            }).done(function (data) {
                $('#searchresult').append(data);
                loadcount += 15;
                inProgress = false;
                $('#loadnextclient').text('Загрузть ещё')
            })
        }
        else {
            $.ajax({
                url: '/client/partiallist/', method: 'GET',
                data: {'loadcount': loadcount, 'full': search_full},
                beforeSend: function () {
                    inProgress = true;
                    $('#loadnextclient').text('Загрузка')
                }
            }).done(function (data) {
                $('#searchresult').append(data);
                loadcount += 15;
                inProgress = false;
                $('#loadnextclient').text('Загрузть ещё')
            })
        }

    });


    $(document).foundation();
    jQuery(function ($) {
    });
});