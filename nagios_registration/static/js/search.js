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

var acc = $(".accordion");
console.log(acc);
console.log(acc[0]);
var i;

for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
        /* Toggle between adding and removing the "active" class,
        to highlight the button that controls the panel */
        this.classList.toggle("active");

        /* Toggle between hiding and showing the active panel */
        var panel = this.nextElementSibling;
        if (panel.style.display === "block") {
            panel.style.display = "none";
        } else {
            panel.style.display = "block";
        }
    });
}
//
$("#delHostModal").on("hide.bs.modal", function() {
    $("#deleteConfirm").off("click");
});