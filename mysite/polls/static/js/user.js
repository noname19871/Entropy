$(document).ready(function () {

    $('#send').click(function(){
        console.log(1);
        var temp = $(":checked")[0].value;
        var numChek = 0;
        switch (temp){
            case 'twitter': 
                break;
            case 'rus':
                numChek = 1;
                break;
            default:  
                numChek = 2;
        }
        var text = $('#text')[0].value;
        $.ajax({
            type: "POST",
            url: "/polls/change_view/",
            data:{
                number: numChek, text: text
            },
            dataType: "json",
            success: function(data){
                    console.log(data.ans);
            }
       });
    });
});