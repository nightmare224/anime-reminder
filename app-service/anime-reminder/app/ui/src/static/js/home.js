$("document").ready(function(){
    // The home page would show all the anime
    $.ajax({
        type: "GET",
        url: "/animereminder/api/v1/user/" + keycloak.user_id + "/anime",
        headers: {"Authorization": "Bearer " + keycloak.access_token }
    }).done(function (rsp) {
        for (var i = 0; i < rsp.length; i++){
            var row = `
            <tr id="${rsp[i].anime_id}tr">
                <td><a href="anime?anime_id=${rsp[i].anime_id}" style="text-decoration: none"><h2>${rsp[i].anime_name}</h2></a></td>
                <td id="deltd"><h3 id="delh1">x<h3></td>
            </tr>`;
            $("#animetb1").append(row);
        }
    });
    // var animelist = ["Spy x Famile", "Chainsaw Man"]
    $("#addanimebtn").click(function(){
        var payload = {
            anime_name: $('input[id=addanimeinput]').val()
        }
        // send anime name to backend
        $.ajax({
            type: "POST",
            url: "/animereminder/api/v1/user/" + keycloak.user_id + "/anime",
            headers: {"Authorization": "Bearer " + keycloak.access_token },
            data: JSON.stringify(payload),
            dataType: "json",
            contentType: "application/json"
        }).done(function (rsp) {
            // add new anime on page
            var row = `
            <tr id="${rsp.anime_id}tr">
                <td><h2>${rsp.anime_name}</h2></td>
                <td class="deltd" id="deltd"><h3 id="delh1">x<h3></td>
            </tr>`;
            $("#animetb1").append(row);
            location.reload();
        });
        // clean the input box
        $('input[id=addanimeinput]').val(' ');
    });
    // $("tr").click(function(){
    //     alert("Clicked");
    //     // window.location.href = "anime.html";
    // });
});