function sendUserVote(voteValue,Url){
    var result = confirm("The vote cannot be changed later!");
    if (result) {
        $.ajax({
            url: Url,
            type:'POST',
            data:{'userVote': voteValue},
            success:function(response){
                window.location.href = response.url;
             }
        })
    }
    else{
        event.preventDefault()
    }
}
