var ids = [
    "schedule"
]
var schedule;

$(function() {
    let data = loadData(ids);
    schedule = data[0];
    console.log(schedule);
    renderSchedule();
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

function createCourseDiv() {
    let p = document.createElement("p");
    return p;
}

function renderSchedule() {
    let p = ['one', 'two', 'three', 'four', 'five', 'six', 'seven'];
    console.log(schedule)
    $.each(schedule, function(day, periods) {
        $.each(periods, function(period, classes) {
            $.each(classes, function(index, class_teacher) {
                let course = class_teacher[0];
                let teacher = class_teacher[1];
                console.log(course, teacher)
                let div = createCourseDiv();
                $(div).text(course + ": " + teacher);
                console.log(div)
                $("." + day.toLowerCase() + " ." + p[period]).append(div);
            })
        })
    })
}