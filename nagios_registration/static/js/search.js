function search() {
    console.log("test");
}

$("#search").on("keyup", function() {
    // Filter logic
    console.log("Alert");
});

// We don't want to trigger the button collapse logic... just the delete logic
 $(document).on('click','#delete_icon',function(e) {
    e.stopPropagation();
 });
