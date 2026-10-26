#include <tuple>
template <typename... Args> auto f(Args...) { return 0; }
int main() {
f(std::make_tuple(1, "x"));
    return 0;
}
