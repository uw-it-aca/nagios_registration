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
    var modal = $(this);
    modal.find('.modal-title').text('Are you sure you want to delete: ' + host + '?');

    $("#deleteConfirm").on("click", function(e) {
        // Ajax call here
        $.ajax({
            url: "ui/api/v1/host/" + host,
            type: 'GET',
            success: function(data) {
                // Load in the data again (refresh the hosts)
                loadData();
            }
        }).fail(function(data) {
            alert("FAILURE");
        });
        $("#delHostModal").modal('hide');
    });
});

//
$("#delHostModal").on("hide.bs.modal", function() {
    $("#deleteConfirm").off("click");
});