/*
        // make the 3As on top of the page clickable and
        // change the text size
        document.getElementById("smallA").onclick = function () {
        changeSize("smallFont");
        };
        document.getElementById("mediumA").onclick = function () {
        changeSize("mediumFont");
        };
        document.getElementById("largeA").onclick = function () {
        changeSize("largeFont");
        };
        function changeSize(size) {
        document.getElementsByTagName("body")[0].className = size;
        }

        // Scroll Bar
        // Reference: https://www.w3schools.com/howto/howto_js_scroll_indicator.asp
        const bar = document.getElementById("scrollBar");

        window.addEventListener("scroll", function () {
        const winScroll =
            document.body.scrollTop || document.documentElement.scrollTop;
        const height =
            document.documentElement.scrollHeight -
            document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        bar.style.width = scrolled + "%";
        });

    Title: CM1040 Web Development, Coursework 2
    Author: The author of this project (Anonoymous submission of assignment)
    Date: March 2022
    Code version: N/A
    Availability: Submitted Assignment (Not published)

    The code below was adapted from the coursework 2 of CM1040 Web Development submitted by the author of this project
*/

// make the 3As on top of the page clickable and
// change the text size
document.getElementById("smallA").onclick = function () {
  changeSize("smallFont");
};
document.getElementById("mediumA").onclick = function () {
  changeSize("mediumFont");
};
document.getElementById("largeA").onclick = function () {
  changeSize("largeFont");
};
function changeSize(size) {
  document.getElementsByTagName("body")[0].className = size;
}

// Scroll Bar
// Reference: https://www.w3schools.com/howto/howto_js_scroll_indicator.asp
const bar = document.getElementById("scrollBar");

window.addEventListener("scroll", function () {
  const winScroll =
    document.body.scrollTop || document.documentElement.scrollTop;
  const height =
    document.documentElement.scrollHeight -
    document.documentElement.clientHeight;
  const scrolled = (winScroll / height) * 100;
  bar.style.width = scrolled + "%";
});
