function search() {
    console.log("test");
}

$("#search").on("keyup", function() {
    // Filter logic
    console.log("Alert");
    var search_val = $("#search").val().toLowerCase();
    console.log(search_val);
    $(".host_box").each(function() {
        var host = $(this);
        var text = host.children(".host_info").text().toLowerCase();
        console.log(text);
        if (!text.includes(search_val)) {
            host.hide();
        } else {
            host.show();
        }
    })
    console.log($(".host_info"));
});