'use strict';
var socket = io("/livefeed");

socket.on('connect', function(data) {
    console.debug("connected!")
});

socket.on('game begin', function(data) {
    console.debug("begin!");
    var gameInfo = data.gameInfo;
    console.debug(gameInfo);
});

socket.on('game result', function(data) {
    console.debug("result!");
    var gameId = data.gameId;
    console.debug(gameId);
    remove_finished(gameId)
});

function add_live(gameInfo) {
    var left_link = $("<a>", {href: '/player/'+gameInfo.player1.pid}).text(gameInfo.player1.name)
    var left = $("<div>", {class: 'player left'}).append(left_link);

    var right_link = $("<a>", {href: '/player/'+gameInfo.player2.pid}).text(gameInfo.player2.name)
    var right = $("<div>", {class: 'player right'}).append(right_link);
    
    var middle = $("<span>", {class: 'middle'}).text("vs.");
    var game_li = $("<li>", {class: 'result', 'id': gameInfo.gameId}).append(left).append(middle).append(right);

    $("#live").prepend(game_li);
    $("#nolive").hide();
}

function remove_finished(gameId) {
    $("#live > li#"+gameId).remove();
    if ($("#live > li").length === 0) {
        $("#nolive").show();
    }
}