#include <array>
#include <cstddef>
auto f(auto...) { return 0; }
int main() {
f(std::array<std::nullptr_t, 0>{});
    return 0;
}
