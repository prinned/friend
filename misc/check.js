'use strict';

var sensor_no = 3
var output_no = 2
var ids       = [[1, 6], [3, 7], [2, 7], [7, 6], [6, 8], [7, 8], [8, 5], [6, 4]]

let act = x => x/2

//inputs should have 1 at start
function genome_forward(inputs, id_list, weights, max_node, act){
    var act_mask = new Array(max_node + 1).fill(0)
    var nodes    = new Array(max_node + 1).fill(0)
    
    for (var i = 0; i < sensor_no + 1; i++) 
        act_mask[i] = 1
        nodes[i] = inputs[i]
    
    for (var i = 0; i < id_list.length; i++){
        
    }

}
var a = [[1, 6], [3, 7], [2, 7], [7, 6], [6, 8], [7, 8], [8, 5], [6, 4]]
for (var i = 0; i < a.length; i++){
    console.log("{", a[i][0], ",", a[i][1], "};");

    
}

//{{1, 6}, {3, 7}, {2, 7}, {7, 6}, {6, 8}, {7, 8}, {8, 5}, {6, 4}}