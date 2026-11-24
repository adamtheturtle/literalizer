#include <array>
#include <cstddef>
template <typename... Args> auto f(Args...) { return 0; }
int main() {
f(std::array<std::nullptr_t, 0>{});
    return 0;
}
