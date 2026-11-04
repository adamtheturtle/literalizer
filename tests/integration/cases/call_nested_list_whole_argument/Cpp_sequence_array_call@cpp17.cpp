#include <array>
#include <variant>
template <typename... Args> auto f(Args...) { return 0; }
int main() {
f(std::array<std::variant<std::array<int, 2>, std::array<int, 1>>, 2>{std::array<int, 2>{1, 2}, std::array<int, 1>{3}});
    return 0;
}
