$(".classes > li").click(togglePref);

function togglePref() {
    if ($(this).hasClass("prefer")) {
        $(this).removeClass("prefer").addClass("indifferent");
    }
    else if ($(this).hasClass("indifferent")) {
        $(this).removeClass("indifferent").addClass("reject");
    }
    else if ($(this).hasClass("reject")) {
        $(this).removeClass("reject").addClass("prefer");
    }
    else {
        $(this).addClass("prefer");
    }
}