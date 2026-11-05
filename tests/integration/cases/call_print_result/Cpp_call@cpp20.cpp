#include <iostream>
auto calculate(auto...) { return 0; }
int main() {
std::cout << calculate(7) << std::endl;
std::cout << calculate(9) << std::endl;
    return 0;
}
