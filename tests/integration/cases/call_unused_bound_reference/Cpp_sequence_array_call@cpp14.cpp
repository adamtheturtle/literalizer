#include <array>
template <typename... Args> auto f(Args...) { return 0; }
int main() {
f(std::array<int, 2>{1, 2});
    return 0;
}
