#include <vector>
#include <iostream>
#include <fstream>
#include <cmath>
#include <assert.h>
#include <array>
#include <random>
#include "neat.h"

void Genome::update_nodes(Connection const& up_connection){
    //i use the "up" prefix to avoid Link-link confusion
    //i.e. all  the good variable names are taken by the struct names
    if (up_connection.disable) return;
    Link up_link = all_links[up_connection.id];
    
    //pushes the connection's in-node to downstream of out-node
    (this->nodes[up_link.out]).incoming_indexes.push_back(up_link.in );
    (this->nodes[up_link.out]).weights.push_back(up_connection.weight);
}

std::vector<Link> Genome::all_links = {};

double Genome::act_func(double const& x){
    return x/2;
}

double Genome::get_value(Node & n){   
    for (int i = 0; i < n.incoming_indexes.size(); i++){
        Node incoming_node = nodes[n.incoming_indexes[i]];

        if (incoming_node.value_is_set) n.value += n.weights[i]*incoming_node.value;
        else n.value += n.weights[i]*get_value(incoming_node);
    }
    
    n.value = act_func(n.value);
    n.value_is_set = true;
    return n.value;
}

Genome::Genome(std::vector<Connection> const& cons, int const& max_node){
    this->cons = cons;
    this->max_node = max_node;
    
    for (int i = 0; i < max_node + 1; i++) {
        this->nodes.push_back({{},{},0,false});
    }
    for (Connection con : this->cons) update_nodes(con);
}

void Genome::clear_nodes(){
    for (Node n : this->nodes){
        n.value = 0;
        n.value_is_set = false;
    }
}

Genome::Genome(Genome const& other_genome){
    cons        = other_genome.cons;
    max_node    = other_genome.max_node;
    nodes       = other_genome.nodes;
}

void Genome::set_value(Node & n, double const& node_value){
    n.value = node_value;
    n.value_is_set = true;
}

std::array<double, Genome::output_no> Genome::forward(std::array<double, sensor_no> const& inputs){

    std::array<double, output_no> out;
    
    set_value(this->nodes[0], 1);
    for (int i = 1; i < sensor_no + 1; i++) set_value(this->nodes[i], inputs[i-1]);

    for (int i = sensor_no + 1; i < sensor_no + output_no + 1; i++){
        set_value(this->nodes[i], get_value(this->nodes[i]));
        out[i - (sensor_no + 1)] = this->nodes[i].value;
    }
    return out;
}

void Genome::new_random_weight(int const& cons_index){
    (this->cons[cons_index]).weight = 
}

void print_node(Node n){
    for (int i : n.incoming_indexes) printf("%i, ", i);
    printf("\n");
    for (double i : n.weights) printf("%g, ", i);
    printf("\nValue: %g\n",  n.value);
    printf("value is set: %i\n\n",  n.value_is_set);
}

int main(){
    srand(time(NULL));

    Genome::all_links.push_back({0, 4});
    Genome::all_links.push_back({2, 4});
    Genome::all_links.push_back({2, 6});
    Genome::all_links.push_back({6, 4});
    Genome::all_links.push_back({7, 5});
    Genome::all_links.push_back({0, 7});
    std::cout<<"CHECK"<<std::endl;
    Genome check({}, 6);
    for (int i = 0; i < Genome::all_links.size(); i++){
        check.update_nodes({i, 1, false});
        check.cons.push_back({i, 1, false});
    }
    //for (double i: check.forward({1, 1, 1})) std::cout<<i<<"\n";
    for (double i = 0; i < 1000; i++) 
    for (double j = 0; j < 100; j++) 
    for (double k = 0; k < 100; k++)
        check.forward({i,j,k});
    std::cout<<"\n\n\n\n";
    //for (Node n: check.nodes) print_node(n);
    //for (double i: check.forward({1, 1, 1}))
    return 0;
}
