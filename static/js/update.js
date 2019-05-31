function submitClicked() {
    var user_url = document.getElementById("id_user_url").value;
    if(!user_url) {
        alert("Kindly enter the url first.")
        return 
    }
    $('#loader').show();
    console.log('update graph called');
    $.ajax({
        url: '/word_cloud', 
        type: 'GET',
        contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
        data: { 
            "user_url": user_url
        },
        success: function (data) {
            console.log("success");
            // returned data is in string format we have to convert it back into json format
            var words_data = $.parseJSON(data);
            console.log(words_data);
            // we will build a word cloud into our div with id=word_cloud
            // we have to specify width and height of the word
            $('#word_cloud').jQCloud('update', words_data);
            $('#loader').hide();
        },
        error: function () {
           alert("error");
           $('#loader').hide();
        }
    });
}
