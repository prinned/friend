#!/usr/bin/env node

'use strict';
var board = [0,0,0,
             0,0,0,
             0,0,0];

function draw(bs){
    var text = "";
    for (var i = 0; i < 9; i++){
        var s;
        if (board[i] === 0)       s = ' ';
        else if (board[i] ===  1) s = 'X';
        else if (board[i] === -1) s = 'O';
        text += "|" + s;
        if (i % 3 == 2) text += "|\n"
    }
    console.log(text);
}

class Network{
    constructor(ni, nh, no){
        this.weights = [[],[]];
        this.nodes   = [[],[],[]];
        
        for (var i = 0; i < ni; i++) this.nodes[0].push(0);
        for (var h = 0; h < nh; h++) this.nodes[1].push(0);
        for (var o = 0; o < no; o++) this.nodes[2].push(0);

        for (var h = 0; h < nh; h++){
            this.weights[0].push([]);
            for (var i = 0; i < ni; i++){
                this.weights[0][h].push(Math.random() - 0.5)
            }
        }

        for (var o = 0; o < no; o++){
            this.weights[1].push([]);
            for (var h = 0; h < nh; h++){
                this.weights[1][o].push(Math.random() - 0.5)
            }
        }
    }

    forward(inputNodes){
        this.Nodes[0] = inputNodes;
        for (var i = 0; i < ni; i++);
    }
}

var check = new Network(1, 1, 1);
