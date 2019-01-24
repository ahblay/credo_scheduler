$("#add-teacher").click(addTeacher);
$("#submit-teacher-form").click(submitTeachers);

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

function submitTeachers() {
    let names = getFieldValues("#teacher-form", ".teacher-name");
    let classes = getFieldValues("#teacher-form", ".eligible-classes");
    let fullTime = getCheckboxValues("#teacher-form", ".full-time");
    let data = {
        "names": names,
        "classes": classes,
        "full_time": fullTime
    }
    $.post("/add_teachers", data);
}