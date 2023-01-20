$("document").ready(function(){
    var url = new URL(document.URL);
    var anime_id = url.searchParams.get('anime_id')
    $.ajax({
        type: "GET",
        url: "/animereminder/api/v1/user/" + keycloak.user_id + "/anime",
        headers: {"Authorization": "Bearer " + keycloak.access_token },
        data: {
            anime_id: anime_id
        }
    }).done(function (rsp) {
        var reminder = rsp[0].anime_reminder;
        for (var i = 0; i < reminder.length; i++){
            var row = `
            <tr>
                <td><h2>${reminder[i].season}</h2></td>
                <td><h2>${reminder[i].episode}</h2></td>
                <td id="deltd"><h3 id="delh1">x<h3></td>
            </tr>`;
            $("#artbbody").append(row);
        }
        // location.reload();
    });
    // // var animelist = ["Spy x Famile", "Chainsaw Man"]
    // $("#addanimebtn").click(function(){

    //     // send anime name to backend
    //     $.ajax({
    //         type: "POST",
    //         url: "/animereminder/api/v1/user/" + keycloak.user_id + "/anime",
    //         headers: {"Authorization": "Bearer " + keycloak.access_token },
    //         data: JSON.stringify(payload),
    //         dataType: "json",
    //         contentType: "application/json"
    //     }).done(function (rsp) {
    //         // add new anime on page
    //         var row = `
    //         <tr id="${rsp.anime_id}tr">
    //             <td><h2>${rsp.anime_name}</h2></td>
    //             <td class="deltd" id="deltd"><h3 id="delh1">x<h3></td>
    //         </tr>`;
    //         $("#animetb1").append(row);
    //         location.reload();
    //     });
    //     // clean the input box
    //     $('input[id=addanimeinput]').val(' ');
    // });
    // // $("tr").click(function(){
    // //     alert("Clicked");
    // //     // window.location.href = "anime.html";
    // // });
});