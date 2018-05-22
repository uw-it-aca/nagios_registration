$(document).ready(function () {
    "use strict";
    $("#search").on("keyup", function() {
        // Filter logic
        var search_val = $("#search").val().toLowerCase();
        $(".host_box").each(function() {
            var host = $(this);
            var text = host.children(".host_info").text().toLowerCase();
            if (!text.includes(search_val)) {
                host.hide();
            } else {
                host.show();
            }
        });
    });
});
