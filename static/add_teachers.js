$("#submit-teacher").click(submitTeachers);
$(".delete-row").click(removeRow);

var ids = [
    "teachers"
]
var teachers;

$(function() {
    let data = loadData(ids);
    teachers = data[0];
    console.log(teachers);
});

function loadData(ids) {
    let data = ids.map(function(id) {
        let item;
        if ($.isEmptyObject($("#" + id + "-data").data(id))) {
            item = {};
        } else {
            item = $.parseJSON($("#" + id + "-data").data(id).replace(/'/g, '"'));
        }
        return item;
    });

    return data;
}

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

function removeRow() {
    $(this).closest("tr").remove();
    let name = $(this).closest("tr").children().first().text();
    let updated_teachers = [];
    let to_delete = [];
    for (let i = 0; i < teachers.length; i++) {
        if (teachers[i][0] != name) {
            updated_teachers.push(teachers[i]);
        }
    }
    teachers = updated_teachers;
    dbDelete(name);
}

function dbDelete(item) {
    let table_name = "teachers";

    let data = {
        "item": item,
        'table_name': table_name
    }

    $.post("/delete", data);
}

