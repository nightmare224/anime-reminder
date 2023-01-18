$("document").ready(function(){
    // The home page would show all the anime
    $.ajax({
        type: "GET",
        url: "/animereminder/api/v1/users",
        headers: {"Authorization": "Bearer " + keycloak.access_token }
    }).done(function (rsp) {
        for (var i = 0; i < rsp.length; i++){
            var row = `<tr><td>${rsp[i].anime_name}</td></tr>`;
            $("#animetb1").append(row);
        }
    });
});