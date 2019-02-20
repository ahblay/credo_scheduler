$(".teachers > li").click(handlePrefs);
$(".classes > li").click(togglePref);

var prefs = $.parseJSON($("#class-prefs").data("class-prefs").replace(/'/g, '"'));
var currentTeacher = null;

console.log(prefs);

function handlePrefs() {
    currentTeacher = $(this).text();
    console.log(currentTeacher);
    let teacherPrefs = prefs[currentTeacher];
    clearPrefs();
    $.each(teacherPrefs, function(k, v) {
        console.log(k, v);
        updatePrefs(k, v);
    })
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

function togglePref() {
    console.log(currentTeacher);
    let course = $(this).attr("id");
    if (currentTeacher == null) {
        return;
    }
    else if ($(this).hasClass("prefer")) {
        $(this).removeClass("prefer").addClass("indifferent");
        if (currentTeacher in prefs) {
            prefs[currentTeacher][course] = 0;
        } else {
            prefs[currentTeacher] = {};
            prefs[currentTeacher][course] = 0;
        }
        submitPrefs(currentTeacher, course, 0);
    }
    else if ($(this).hasClass("indifferent")) {
        $(this).removeClass("indifferent").addClass("reject");
        if (currentTeacher in prefs) {
            prefs[currentTeacher][course] = -1;
        } else {
            prefs[currentTeacher] = {};
            prefs[currentTeacher][course] = -1;
        }
        submitPrefs(currentTeacher, course, -1);
    }
    else if ($(this).hasClass("reject")) {
        $(this).removeClass("reject").addClass("prefer");
        if (currentTeacher in prefs) {
            prefs[currentTeacher][course] = 1;
        } else {
            prefs[currentTeacher] = {};
            prefs[currentTeacher][course] = 1;
        }
        submitPrefs(currentTeacher, course, 1);
    }
    else {
        $(this).addClass("prefer");
        if (currentTeacher in prefs) {
            prefs[currentTeacher][course] = 1;
        } else {
            prefs[currentTeacher] = {};
            prefs[currentTeacher][course] = 1;
        }
        submitPrefs(currentTeacher, course, 1);
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
