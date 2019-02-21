$("#submit-class").click(submitClass);

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

    //updateClassList(name, subject, type, hours);

    let data = {
        "name": name,
        "subject": subject,
        "type": type,
        "hours": hours
    }
    $.post("/add_classes", data);
}

function updateClassList(name, subject, type, hours) {
    let data = [name, subject, type, hours];
    classes.push(data);

    li = $(document).createElement("li");
    $(li).text(name);
    $("#classes").append(li);
}