(function($) {
    $.ajax(base_url + "/api/v1/host", {
        success: function() {
            var hostlist_source = $("#host_list_template").html();
            var tmpl = Handlebars.compile(hostlist_source);
            $("#hosts").html(tmpl({ hosts: arguments[0] }));

        }
    });
})(jQuery);
