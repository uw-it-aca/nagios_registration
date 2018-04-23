function search() {
    console.log("test");
}

$("#search").on("keyup", function() {
    // Filter logic
    console.log("Alert");
});


$('i').click(function(e) {
    console.log("Delete");
    $("#my_modal").show();
});