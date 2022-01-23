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
});