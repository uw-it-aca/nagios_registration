function search() {
    console.log("test");
}

$("#search").on("keyup", function() {
    // Filter logic
    console.log("Alert");
});

for (var i = 0; i < $(".accordion").length; i++) {
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

$("#delete_icon").on("click", function(e) {
    console.log("here");
    e.preventDefault();
});
console.log($("#delete_icon"));