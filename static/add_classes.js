$("#submit-class").click(submitClass);
$(".delete-row").click(removeRow);

var classes;
if ($.isEmptyObject($("#class-data").data("classes"))) {
    classes = [];
} else {
    classes = $.parseJSON($("#class-data").data("classes").replace(/'/g, '"'));
}
console.log(classes);

function submitClass() {
    let name = $("#class-name").val();
    let subject = $("#class-subject").val();
    let type = $("#class-type").val();
    let hours = $("#class-hours").val();

    let data = {
        "name": name,
        "subject": subject,
        "type": type,
        "hours": hours
    }
    $.post("/add_classes", data);
}

function removeRow() {
    $(this).closest("tr").remove();
    let name = $(this).closest("tr").children().first().text();
    let updated_classes = [];
    let to_delete = [];
    for (let i = 0; i < classes.length; i++) {
        if (classes[i][0] != name) {
            updated_classes.push(classes[i]);
        }
    }
    classes = updated_classes;
    dbDelete(name);
}

function dbDelete(item) {
    let table_name = "classes";

    let data = {
        "item": item,
        'table_name': table_name
    }

    $.post("/delete", data);
}
