//#include <algorithm>
#include <vector>
#include <iostream>
#include <fstream>
#include <cmath>
#include <assert.h>


//HEADER -

template <typename T>
void print_array(T a, int length){
    printf("{");
    for (int i = 0; i < length - 1; i++) std::cout<< a[i]<< ", ";
    std::cout<< a[length - 1] << "}\n";
}

class Genome{
public:
    static std::vector<int> all_in;
    static std::vector<int> all_out;
    static int sensor_no;
    static int output_no;
    
    int max_node;
    double* nodes; 
    std::vector<int> id_list;
    std::vector<bool> disable_mask;
    std::vector<double> weights; 

    Genome(std::vector<int> const& id_list, std::vector<double> const& weights, std::vector<bool> const& disable_mask, int const& max_node);
    ~Genome();
    static double act_func(double const& x);
    static bool equal_connections(int* const& con1, int* const& con2);
    void forward(int* const& inputs);
};
//HEADER -

std::vector<int> Genome::all_in ({ 1,3,2,7,6,7,8,6 });
std::vector<int> Genome::all_out({ 6,7,7,6,8,8,5,4 });
int Genome::sensor_no = 3;
int Genome::output_no = 2;

Genome::Genome(std::vector<int>  const& id_list, std::vector<double> const& weights,
               std::vector<bool> const& disable_mask, int const& max_node){
    this->id_list = id_list;
    this->weights = weights;
    this->disable_mask = disable_mask;
    this->max_node = max_node;

    this->nodes = new double[max_node + 1];
    nodes[0] = 1;
    print_array(nodes, max_node + 1);
}

double Genome::act_func(double const& x){
    //return 1/(1 + std::exp(-x));
    return x/2;
}

Genome::~Genome(){
    delete[] this->nodes;
}

bool Genome::equal_connections(int* const& con1, int* const& con2) {
    return (con1[0] == con2[0] && con1[1] == con2[1]);
}



void Genome::forward(int* const& inputs){
    //act_mask: if 1, then already activated
    //          if 0, needs to activateeeeee
    bool* act_mask = new bool[max_node + 1];
    act_mask[0] = 1;
    for (int i = 1; i < sensor_no + 1;  i++) {
        nodes[i] = inputs[i - 1];
        act_mask[i] = 1;
    }
    for (int i = 0; i < id_list.size(); i++){
        if (disable_mask[i]) continue;
        int from_nodex = all_in[ id_list[i]];
        int   to_nodex = all_out[id_list[i]];
        if (act_mask[from_nodex] == false){
            nodes[from_nodex] = Genome::act_func(nodes[from_nodex]);
            act_mask[from_nodex] = true;
        }

        assert(act_mask[to_nodex] == false);
        nodes[to_nodex] += weights[i]*nodes[from_nodex];
        //printf("%i, %i\n", from_node, to_node);
        //print_array(nodes, max_node+1);
    }
    print_array(nodes, max_node + 1);
    for (int i = sensor_no + 1; i <= sensor_no + output_no; i++) {
        nodes[i] = Genome::act_func(nodes[i]);
    }
    print_array(nodes, max_node + 1);
}

int main(){
    
    Genome g1({0,1,2,3,4,5,6,7}, {1,1,1,1,1,1,1,1}, {0,0,0,0,0,0,0,0}, 8);
    
    //g1.forward(input);
    g1.forward( new int[3]{1,0,0} );
    print_array(g1.nodes, g1.max_node + 1);
    return 0;
}