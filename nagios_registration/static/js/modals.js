
$("#delHostModal").modal({
  "backdrop"  : "static",
  "keyboard"  : true,
  "show"      : false,
});

$("#delServiceModal").modal({
  "backdrop"  : "static",
  "keyboard"  : true,
  "show"      : false,
});

$("#delServiceModal").on("show.bs.modal", function(event) {
    var trigger = $(event.relatedTarget);
    var host = trigger.data('host');
    var service = trigger.data('service');
    var modal = $(this);
    modal.find('.modal-title').html('Are you sure you want to delete: <code>' + service + '</code> from <code>' + host + '</code>?');

    $("#delServiceConfirm").on("click", function(e) {
        // Ajax call here
        $.ajax({
            url: "/api/v1/service/" + host + "/" + service,
            type: 'DELETE',
            success: function(data) {
                // Load in the data again (refresh the hosts)
                loadData();
            }
        }).fail(function(data) {
            alert("FAILURE");
        });
        $("#delServiceModal").modal('hide');
    });
});


$("#delHostModal").on("show.bs.modal", function(event) {
    var trigger = $(event.relatedTarget);
    var host = trigger.data('host');
    var modal = $(this);
    modal.find('.modal-title').html('Are you sure you want to delete: <code>' + host + '</code>?');

    $("#delHostConfirm").on("click", function(e) {
        // Ajax call here
        $.ajax({
            url: "/api/v1/host/" + host,
            type: 'DELETE',
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

$("#delHostModal").on("hide.bs.modal", function() {
    $("#delHostConfirm").off("click");
});

$("#delServiceModal").on("hide.bs.modal", function() {
    $("#delServiceConfirm").off("click");
});

// We don't want to trigger the button collapse logic... just the delete logic
 $(document).on('click','#delete_icon',function(e) {
    e.stopPropagation();
 });


