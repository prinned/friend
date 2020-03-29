#include <vector>
#include <iostream>
#include <cmath>
#include <random>


int r(){
    return std::rand() ;
}

int main(){
    //
    
    srand(time(NULL));
    std::cout<< r();
    return 0;
}
