#pragma once

#include <vector>
#include <iostream>
#include <fstream>
#include <cmath>
#include <assert.h>
#include <array>

struct Connection{
    int id;
    double weight;
    bool disable;
};

struct Link{
    int in, out;
};

//struct vs class purely aesthetic (i hope)
//you can change struct to class as long as you add "public:"
struct Node{
    std::vector<int> incoming_indexes;
    std::vector<double> weights;
    double value; //initially unset!
    bool value_is_set = false;
};


class Genome{
public:
    std::vector<Connection> cons;
    std::vector<Node> nodes;
    int max_node;
    
    static std::vector<Link> all_links;
    static double act_func(double const& x);
    static constexpr int sensor_no = 3;
    static constexpr int output_no = 2;
    
    Genome(Genome const& other_genome);
    Genome(std::vector<Connection> const& cons, int const& max_node);
    std::array<double, output_no> forward(std::array<double, sensor_no> const& inputs);
    
    //Node manipulation
    void update_nodes(Connection const& con);
    void clear_nodes();
    double get_value(Node & n);
    void set_value(Node & n, double const& node_value);

    //Mutation 
    void new_random_weight(int const& cons_index);
    void change_weight(int const&  cons_index);
    void switch_con_disability(int const& cons_index);
    void add_connection(int const& nodex1, int const&  nodex2);
    void add_node(int const& cons_index);



};
