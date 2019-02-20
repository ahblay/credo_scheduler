$(".teachers > li").click(handlePrefs);
$(".classes > li").click(togglePref);

var prefs = $("#class-prefs").data();
var currentTeacher = null;

console.log(prefs);

function handlePrefs() {
    currentTeacher = $(this).text();
    console.log(currentTeacher);
    let teacherPrefs = prefs[currentTeacher];
    $.each(teacherPrefs, function(k, v) {
        console.log(k, v);
        updatePrefs(k, v);
    })
}

function updatePrefs(course, pref) {
    if (pref == -1) {
        $("#" + course).removeClass().addClass("reject");
    }
    else if (pref == 0) {
        $("#" + course).removeClass().addClass("indifferent");
    }
    else if (pref == 1) {
        $("#" + course).removeClass().addClass("prefer");
    }
    else {
        $("#" + course).removeClass();
    }
}

function togglePref() {
    console.log(currentTeacher);
    let course = $(this).attr("id");
    if (currentTeacher == null) {
        return;
    }
    else if ($(this).hasClass("prefer")) {
        $(this).removeClass("prefer").addClass("indifferent");
        submitPrefs(currentTeacher, course, 0);
    }
    else if ($(this).hasClass("indifferent")) {
        $(this).removeClass("indifferent").addClass("reject");
        submitPrefs(currentTeacher, course, -1);
    }
    else if ($(this).hasClass("reject")) {
        $(this).removeClass("reject").addClass("prefer");
        submitPrefs(currentTeacher, course, 1);
    }
    else {
        $(this).addClass("prefer");
        submitPrefs(currentTeacher, course, 1);
    }
}

function submitPrefs(teacher, course, pref) {
    let data = {
        "teacher": teacher,
        "class": course,
        "pref": pref
    }
    $.post("/prefs", data);
}
