$("document").ready(function(){
    var url = new URL(document.URL);
    var anime_id = url.searchParams.get('anime_id')
    $.ajax({
        type: "GET",
        url: "/animereminder/api/v1/user",
        headers: {"Authorization": "Bearer " + keycloak.access_token }
    }).done(function (rsp) {
        for (var i = 0; i < rsp.length; i++){
            var row = `
            <tr class="artbtr">
                <td class="season"><h2><a href="#edituser" rel="modal:open" style="text-decoration: none">${rsp[i].user_id}</a></h2></td>
                <td class="deltd" id="deltd"><h3 class="delh1">x<h3></td>
            </tr>`;
            $("#usertbbody").append(row);
        }
    });
    // bind the future td
    $("#usertbbody").on('click', 'td', function(){

    })
    $("#usertbbody").on('click', '.deltd', function(){
        // let season = $(this).siblings(".season").text();
        // let episode = $(this).siblings(".episode").text();
        // let payload = {
        //     "anime_reminder": [
        //         {
        //             "season": season,
        //             "episode": episode
        //         }
        //     ]
        // }
        // $.ajax({
        //     type: "DELETE",
        //     url: "/animereminder/api/v1/user/" + keycloak.user_id + "/anime/" + anime_id + "/reminder",
        //     headers: {"Authorization": "Bearer " + keycloak.access_token },
        //     data: JSON.stringify(payload),
        //     dataType: "json",
        //     contentType: "application/json"
        // }).done(function (rsp) {
        //     location.reload();
        // });
    })
    // $("#addarbtn").click(function(){
    //     let payload = {
    //         "anime_reminder": [
    //             {
    //                 "season": sspinner.spinner("value").toString(),
    //                 "episode": espinner.spinner("value").toString()
    //             }
    //         ]
    //     }
    //     $.ajax({
    //         type: "PUT",
    //         url: "/animereminder/api/v1/user/" + keycloak.user_id + "/anime/" + anime_id + "/reminder",
    //         headers: {"Authorization": "Bearer " + keycloak.access_token },
    //         data: JSON.stringify(payload),
    //         dataType: "json",
    //         contentType: "application/json"
    //     }).done(function (rsp) {
    //         location.reload();
    //     });
    // });
});