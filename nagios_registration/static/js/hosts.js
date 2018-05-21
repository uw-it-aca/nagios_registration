function loadData() {
    $.ajax(base_url + "/api/v1/data", {
        success: function(hosts) {
            var hostlist_source = $("#host_list_template").html();
            var tmpl = Handlebars.compile(hostlist_source);
            $("#hosts").html(tmpl({ hosts: hosts }));
        }
    });
}

$( document ).ready(function() {
    loadData();
});