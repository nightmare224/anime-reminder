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
            <tr class="artbtr">
                <td class="season"><h2><a href="#addar" rel="modal:open" style="text-decoration: none">${reminder[i].season}</a></h2></td>
                <td class="episode"><h2><a href="#addar" rel="modal:open" style="text-decoration: none">${reminder[i].episode}</a></h2></td>
                <td class="deltd" id="deltd"><h3 class="delh1">x<h3></td>
            </tr>`;
            $("#artbbody").append(row);
        }
    });
    var sspinner = $("#sspinner").spinner();
    var espinner = $("#espinner").spinner();
    $("#addartr").click(function(){
        sspinner.spinner("enable")
        espinner.spinner("enable")
    })
    // bind the future td
    $("#artbbody").on('click', 'td', function(){
        // season always disable no matter what it click
        if ( $(this).attr("class") === "season" ) {
            sspinner.spinner("disable")
            espinner.spinner("enable")
            sspinner.spinner("value", $(this).text());
            espinner.spinner("value", $(this).siblings(".episode").text());
            
        } else if ( $(this).attr("class") === "episode" ) {
            espinner.spinner("enable")
            sspinner.spinner("disable")
            espinner.spinner("value", $(this).text());
            sspinner.spinner("value", $(this).siblings(".season").text());
        }
    })
    $("#artbbody").on('click', '.deltd', function(){
        let season = $(this).siblings(".season").text();
        let episode = $(this).siblings(".episode").text();
        let payload = {
            "anime_reminder": [
                {
                    "season": season,
                    "episode": episode
                }
            ]
        }
        $.ajax({
            type: "DELETE",
            url: "/animereminder/api/v1/user/" + keycloak.user_id + "/anime/" + anime_id + "/reminder",
            headers: {"Authorization": "Bearer " + keycloak.access_token },
            data: JSON.stringify(payload),
            dataType: "json",
            contentType: "application/json"
        }).done(function (rsp) {
            location.reload();
        });
    })
    $("#addarbtn").click(function(){
        $(this).addClass("is_active");
        $(this).animate({opacity: 1}, 500, function(){
            let payload = {
                "anime_reminder": [
                    {
                        "season": sspinner.spinner("value").toString(),
                        "episode": espinner.spinner("value").toString()
                    }
                ]
            }
            $.ajax({
                type: "PUT",
                url: "/animereminder/api/v1/user/" + keycloak.user_id + "/anime/" + anime_id + "/reminder",
                headers: {"Authorization": "Bearer " + keycloak.access_token },
                data: JSON.stringify(payload),
                dataType: "json",
                contentType: "application/json"
            }).done(function (rsp) {
                location.reload();
            });
        });

    });
});