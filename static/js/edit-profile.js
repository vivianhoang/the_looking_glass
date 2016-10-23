var maxLength = 1000;

$('.profile-bio').keyup(function() {
    var length = $(this).val().length;
    var new_length = maxLength-length;
    $('.chars').text(new_length);
});

$('.past-job').keyup(function() {
    var length = $(this).val().length;
    var new_length = maxLength-length;
    $('.chars').text(new_length);
});

function showConfirmation(result) {
    alert(result);
}

function updateProfile(evt) {
    evt.preventDefault();

    var formInputs = {
        "category-id": $(".category").val(),
        "company": $(".company-name").val(),
        "description": $(".profile-bio").val(),
        "prev-experience": $(".past-job").val(),
        "city": $(".city").val(),
        "url": $(".url").val()
    };

    console.log(formInputs);

    $.post("/profile-edit",
        formInputs,
        showConfirmation
        );
}

$("#profile-description").on("submit", updateProfile);