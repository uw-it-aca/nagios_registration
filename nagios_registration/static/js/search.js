function search() {
    console.log("test");
}

$("#search").on("keyup", function() {
    // Filter logic
    console.log("Alert");
});


$("#delHostModal").modal({
  "backdrop"  : "static",
  "keyboard"  : true,
  "show"      : false,
});


$("#delHostModal").on("show.bs.modal", function(event) {
    var trigger = $(event.relatedTarget);
    var host = trigger.data('host');
    var modal = $(this)
    modal.find('.modal-title').text('Are you sure you want to delete: ' + host + '?');

    $("#deleteConfirm").on("click", function(e) {
        // Ajax call here
        $("#delHostModal").modal('hide');
    });
});