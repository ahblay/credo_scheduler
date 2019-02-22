//$("#add-teacher").click(addTeacher);
$("#submit-teacher").click(submitTeachers);

var teachers;
if ($.isEmptyObject($("#teacher-data").data("teachers"))) {
    teachers = [];
} else {
    teachers = $.parseJSON($("#teacher-data").data("teachers").replace(/'/g, '"'));
}
console.log(teachers);

function submitTeachers() {
    let name = $("#teacher-name").val();
    let classes = $("#teacher-classes").val();
    let fullTime;
    if ($("#teacher-type").is(":checked")) {
        fullTime = true;
    } else {
        fullTime = false;
    }

    let data = {
        "name": name,
        "classes": classes,
        "full_time": fullTime
    }
    console.log(data)
    $.post("/add_teachers", data);
}

/*
function addTeacher() {
    let teacherForm = $("#teacher-form > .form-row").clone().slice(0, 2);
    for (i = 0; i < teacherForm.length; i++) {
        $(teacherForm[i]).find("input").val('').prop("checked", false);
    };
    teacherForm.appendTo("#teacher-form");
};

function getFieldValues(formSelector, fieldSelector) {
    let values = [];
    $(formSelector).find(fieldSelector).map(function() {
        values.push($(this).val());
    });
    return values;
}

function getCheckboxValues(formSelector, fieldSelector) {
    let values = [];
    $(formSelector).find(fieldSelector).map(function() {
        if ($(this).is(":checked")) {
            values.push(true);
        } else {
            values.push(false);
        }
    });
    return values;
}
*/