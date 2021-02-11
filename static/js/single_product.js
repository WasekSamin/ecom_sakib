// Product magnifier starts
// Create a condition that targets viewports at least 768px wide
const mediaQuery = window.matchMedia('(min-width: 992px)')

function handleTabletChange(e) {
  // Check if the media query is true
  if (e.matches) {
    // Then log the following message to the console
    $("#featured").elevateZoom({
        easing: true,
        cursor: "crosshair"
    });
  } else if (window.innerWidth >= 768 && window.innerWidth < 992) {
    $("#featured").elevateZoom({
        zoomType: "inner",
        easing: true,
        cursor: "crosshair"
    });
  }
}
// Register event listener
mediaQuery.addListener(handleTabletChange)

// Initial check
handleTabletChange(mediaQuery)
// Product magnifier ends



// Slider event starts
$(document).ready(function() {
    let thumbnails = document.getElementsByClassName("thumbnail");
    let activeImages = document.getElementsByClassName("active");

    for (let i=0; i<thumbnails.length; i++) {
        thumbnails[i].addEventListener("click", function() {
            if (activeImages.length > 0) {
                activeImages[0].classList.remove("active");
            }

            this.classList.add("active");
            document.getElementById("featured").src = this.src;
            $("#featured").elevateZoom({
                easing: true,
                cursor: "crosshair"
            });
        });
    }

});