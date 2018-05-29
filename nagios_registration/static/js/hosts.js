function loadData() {
    $.ajax("/api/v1/host", {
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
