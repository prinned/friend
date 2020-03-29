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


//STOPPING USERS FROM HAVING INPUTS AND OUTPUTS MORE THAN 255
template <uint8_t sensor_no, uint8_t output_no>
class Genome{
public:
    std::vector<Connection> cons;
    std::vector<Node> nodes;
    int max_node;
    
    static std::vector<Link> all_links;
    static double act_func(double const& x);
    
    Genome(Genome const& other_genome);
    Genome(std::vector<Connection> const& cons, int const& max_node);
    void update_nodes(Connection const& con);
    void clear_nodes();
    double get_value(Node & n);
    std::array<double, output_no> forward(std::array<double, sensor_no> const& inputs);
};

template <uint8_t s, uint8_t o>
void Genome<s, o>::update_nodes(Connection const& up_connection){
    //i use the "up" prefix to avoid Link-link confusion
    //i.e. all  the good variable names are taken by the struct names
    if (up_connection.disable) return;
    Link up_link = all_links[up_connection.id];
    
    //pushes the connection's in-node to downstream of out-node
    (this->nodes[up_link.out]).incoming_indexes.push_back(up_link.in );
    (this->nodes[up_link.out]).weights.push_back(up_connection.weight);
}

template <uint8_t s, uint8_t o>
std::vector<Link> Genome<s, o>::all_links = {};

template <uint8_t s, uint8_t o>
double Genome<s, o>::act_func(double const& x){
    return x/2;
}

template <uint8_t s, uint8_t o>
double Genome<s, o>::get_value(Node & n){   
    for (int i = 0; i < n.incoming_indexes.size(); i++){
        Node incoming_node = nodes[n.incoming_indexes[i]];

        if (incoming_node.value_is_set) n.value += n.weights[i]*incoming_node.value;
        else n.value += n.weights[i]*get_value(incoming_node);
    }
    
    n.value = act_func(n.value);
    n.value_is_set = true;
    return n.value;
}

template <uint8_t s, uint8_t o>
Genome<s, o>::Genome(std::vector<Connection> const& cons, int const& max_node){
    this->cons = cons;
    this->max_node = max_node;
    
    //for (Connection con : this->cons) update_nodes(con);
}

template <uint8_t s, uint8_t o>
void Genome<s, o>::clear_nodes(){
    for (Node n : this->nodes){
        n.value = 0;
        n.value_is_set = false;
    }
}

template <uint8_t s, uint8_t o>
Genome<s, o>::Genome(Genome const& other_genome){
    cons        = other_genome.cons;
    max_node    = other_genome.max_node;
    nodes       = other_genome.nodes;
}

template <uint8_t s, uint8_t o>
std::array<double, o> Genome<s, o>::forward(std::array<double, s> const& inputs){
    std::array<double, o> out;
    for (int i = s + 1; i < s + o + 1; i++){
        out[i - (s + 1)] = get_value(this->nodes[i]);
    }
    return out;
}

int main(){
    Genome<3, 2> check({}, 5);
    Genome<3, 2>::all_links.push_back({0, 0});

    return 0;
}

/*
class Node{
public:
    static std::vector<Node> node_list;

    std::vector<int> incoming_index;
    std::vector<float> weights;
    double value; //initially unset!
    bool value_is_set = false;

    double get_value(){   
        for (int i = 0; i < incoming.size(); i++){
            Node incoming_node = node_list[incoming_index[i]]
            if (incoming[i].value_is_set) value += weights[i]*incoming[i].value;
            else value += weights[i]*incoming[i].get_value();
        }
        value_is_set = true;
        return value;
    }

    double test_for_recursion(){
        
        for (int i = 0; i < incoming.size(); i++){
            if (incoming[i].value_is_set) value += weights[i]*incoming[i].value;
            else value += weights[i]*incoming[i].get_value();
        }
        value_is_set = true;
    }
};
*/