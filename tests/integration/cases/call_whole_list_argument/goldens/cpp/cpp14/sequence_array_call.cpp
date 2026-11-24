#include <array>
template <typename... Args> auto f(Args...) { return 0; }
int main() {
f(std::array<int, 1>{1});
    return 0;
}
