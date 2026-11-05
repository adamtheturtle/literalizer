#include <iostream>
template <typename... Args> auto calculate(Args...) { return 0; }
int main() {
std::cout << calculate(7) << '\n';
std::cout << calculate(9) << '\n';
    return 0;
}
