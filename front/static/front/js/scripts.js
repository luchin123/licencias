(function($) {

    // Persona autocompletar.
    var opcionesPersona = {
        minLength: 1,
        open: function() {
            var acData = $(this).data('uiAutocomplete');
            acData
                .menu
                .element
                .find('li')
                .each(function () {
                    var me = $(this);
                    var keywords = acData.term.split(' ').join('|');
                    me.html(me.text().replace(new RegExp("(" + keywords + ")", "gi"), '<strong class="text-danger">$1</strong>'));
             });;
        },
        source: function(request, response) {
            $.ajax({
                url: '/api/base/persona/filter/',
                dataType: 'json',
                data: {
                    term: request.term
                },
                success: function(data, e) {
                    if(e)
                    response($.map(data, function (item) {
                        return {
                            data: item,
                            label: item.dni + ' - ' + item.nombres + ' ' + item.apellidos,
                            value: item.nombres + ' ' + item.apellidos
                        }
                    }));
                }
            })
        },
        response: function(e, ui) {
            if(ui.content.length === 0) {
                //$('.alert-cliente').show();
                var parent = $(e.target).parent();
                parent.find('.ac-persona').val('');
                $('#id_persona').val('');
            }
        },
        select: function(e, ui) {
            e;
            $('#id_persona').val(ui.item.data.id);
        },
        change: function(e,ui) {
            if(!ui.item) {
                //$('.alert-cliente').show();
                var parent = $(e.target).parent();
                parent.find('.ac-persona').val('');
                $('#id_persona').val('');
            }
        }
    };

    $('.ac-persona').autocomplete(opcionesPersona);

    // Fechas.
    var datepickerOptions = {
        changeMonth: true,
        changeYear: true,
        dateFormat: 'dd-mm-yy'
    };

    $('.datepicker').datepicker(datepickerOptions);
})(jQuery);
