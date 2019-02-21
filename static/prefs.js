$(".teachers > li").click(handlePrefs);
$(".classes > li").click(togglePref);

var prefs;
if ($.isEmptyObject($("#class-prefs").data("class-prefs"))) {
    prefs = {};
} else {
    prefs = $.parseJSON($("#class-prefs").data("class-prefs").replace(/'/g, '"'));
}
var currentTeacher = null;

console.log(prefs);

function handlePrefs() {
    currentTeacher = $(this).text();
    let teacherPrefs = prefs[currentTeacher];

    toggleSelected($(this));
    clearPrefs();
    $.each(teacherPrefs, function(k, v) {
        updatePrefs(k, v);
    })
}

function toggleSelected(li) {
    $(".teachers > li").each(function() {
        $(this).removeClass("selected");
    })
    li.addClass("selected");
}

function clearPrefs() {
    $(".classes > li").each(function() {
        $(this).removeClass("reject indifferent prefer");
    })
}

function updatePrefs(course, pref) {
    if (pref == -1) {
        $("#" + course).removeClass("reject indifferent prefer").addClass("reject");
    }
    else if (pref == 0) {
        $("#" + course).removeClass("reject indifferent prefer").addClass("indifferent");
    }
    else if (pref == 1) {
        $("#" + course).removeClass("reject indifferent prefer").addClass("prefer");
    }
    else {
        $("#" + course).removeClass("reject indifferent prefer");
    }
}

function handleToggle(pref, course) {
    let val;
    if (pref == "reject") {
        val = -1;
    }
    else if (pref == "indifferent") {
        val = 0;
    } else {
        val = 1;
    }
    if (currentTeacher in prefs) {
        prefs[currentTeacher][course] = val;
    } else {
        prefs[currentTeacher] = {};
        prefs[currentTeacher][course] = val;
    }
    submitPrefs(currentTeacher, course, val);
}

function togglePref() {
    console.log(currentTeacher);
    let course = $(this).attr("id");
    if (currentTeacher == null) {
        return;
    }
    else if ($(this).hasClass("prefer")) {
        $(this).removeClass("prefer").addClass("indifferent");
        handleToggle("indifferent", course);
    }
    else if ($(this).hasClass("indifferent")) {
        $(this).removeClass("indifferent").addClass("reject");
        handleToggle("reject", course);
    }
    else if ($(this).hasClass("reject")) {
        $(this).removeClass("reject").addClass("prefer");
        handleToggle("prefer", course);
    }
    else {
        $(this).addClass("prefer");
        handleToggle("prefer", course);
    }
}

function submitPrefs(teacher, course, pref) {
    let data = {
        "teacher": teacher,
        "class": course,
        "pref": pref
    }
    console.log(data)
    $.post("/prefs", data);
}
