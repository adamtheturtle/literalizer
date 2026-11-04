#include <cstddef>
#include <vector>
template <typename... Args> auto f(Args...) { return 0; }
int main() {
f(std::vector<std::nullptr_t>{});
    return 0;
}
