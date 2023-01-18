// function sayHello(){
//     alert("Hello World");
// }
$.ajax({
    type: "GET",
    url: "/animereminder/api/v1/users",
}).done(function (rsp) {
    alert(rsp);
});

allAnimeTable(allAnime)
$(document).ready(function (){
    let dt = $('#allAnimeTable').DataTable();
    dt.clear().draw();
    dt.row.add(['spy famile']).draw();
    // alert(table);
    // for (var i = 0; i < data.length; i++){
    //     // var row = `<tr><td>${data[i].name}</td></tr>`;
    //     // table.innerHTML += row;
    //     table.row.add(['spy famile']).draw(true);
    // }
})
