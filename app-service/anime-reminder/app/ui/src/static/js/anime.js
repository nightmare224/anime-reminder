$("document").ready(function(){
    var url = new URL(document.URL);
    var anime_id = url.searchParams.get('anime_id')
    $.ajax({
        type: "GET",
        url: "/animereminder/api/v1/user/" + keycloak.user_id + "/anime",
        headers: {"Authorization": "Bearer " + keycloak.access_token },
        data: {
            "anime_id": anime_id
        }
    }).done(function (rsp) {
        var reminder = rsp[0].anime_reminder;
        for (var i = 0; i < reminder.length; i++){
            var row = `
            <tr>
                <td><h2><a href="#addar" rel="modal:open" style="text-decoration: none">${reminder[i].season}</a></h2></td>
                <td><h2><a href="#addar" rel="modal:open" style="text-decoration: none">${reminder[i].episode}</a></h2></td>
                <td id="deltd"><h3 id="delh1">x<h3></td>
            </tr>`;
            $("#artbbody").append(row);
        }
        // location.reload();
    });
    var sspinner = $("#sspinner").spinner();
    var espinner = $("#espinner").spinner();
    // // var animelist = ["Spy x Famile", "Chainsaw Man"]
    $("#addarbtn").click(function(){
        var payload = {
            "anime_reminder": [
                {
                    "season": sspinner.spinner("value").toString(),
                    "episode": espinner.spinner("value").toString()
                }
            ]
        }
        $.ajax({
            type: "PUT",
            url: "/animereminder/api/v1/user/" + keycloak.user_id + "/anime/" + anime_id,
            headers: {"Authorization": "Bearer " + keycloak.access_token },
            data: JSON.stringify(payload),
            dataType: "json",
            contentType: "application/json"
        }).done(function (rsp) {
            location.reload();
        });
        // // clean the input box
        // $('input[id=addanimeinput]').val(' ');
    });
    // // $("tr").click(function(){
    // //     alert("Clicked");
    // //     // window.location.href = "anime.html";
    // // });
});