#include <vector>
#include <iostream>

void pb(std::vector<int> a){
    for (int i = 0; i < a.size(); i++) std::cout<<a[i]<<" ";
    std::cout<<"\n";
}

void f(int const& a){
    std::cout<<"CHECK "<<a<<"\n";
}

int main(){
    int* a = new int[10];
    a = new int[10]({0,1,2,3,1,4,5,3,4,5});
    return 0;
}