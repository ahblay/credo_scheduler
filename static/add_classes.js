$("#add-subj").click(addCard);

function addCard() {
    let card = generateCard();
    $(".classes").append(card);
}

function generateCard() {
    let cardMain = document.createElement("div");
    let cardHeader = document.createElement("h5");
    let cardList = document.createElement("ul");

    $(cardMain).addClass("card");
    $(cardHeader).addClass("card-header");
    $(cardList).addClass("list-group").addClass("list-group-flush");

    $(cardHeader).html("SAMPLE HEADER");
    $(cardMain).css("width", "18rem");

    $(cardMain).append(cardHeader).append(cardList);

    return cardMain;
}