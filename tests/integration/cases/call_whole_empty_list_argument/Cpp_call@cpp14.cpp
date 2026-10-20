#include <initializer_list>
#include <vector>
#include <cstddef>
template <typename... Args> auto f(Args...) { return 0; }
int main() {
f(std::vector<std::nullptr_t>{});
    return 0;
}
