/**
 * The function sends a user's vote value and URL to a server using AJAX, and redirects the user to a
 * new page based on the server's response.
 * @param voteValue - The vote value is the value that the user wants to submit as their vote. It could
 * be a number, a string, or any other data type that represents the user's vote.
 * @param Url - The `Url` parameter is the URL where the vote will be sent to. It is the endpoint or
 * route on the server that will handle the vote submission.
 */
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
