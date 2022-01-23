'use strict';
var socket = io("/livefeed");

socket.on('after connect', function(data) {
    console.debug("connected!")
});

socket.on('game_begin', function(data) {
    console.debug("begin!");
    var gameInfo = data.gameInfo;
    console.debug(gameInfo);
});

socket.on('game_result', function(data) {
    console.debug("result!");
    var gameId = data.gameId;
    console.debug(gameId);
});