#include <array>
auto f(auto...) { return 0; }
int main() {
f(std::array<int, 2>{1, 2});
    return 0;
}
