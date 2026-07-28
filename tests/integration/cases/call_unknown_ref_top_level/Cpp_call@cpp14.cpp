#include <initializer_list>
#include <vector>
#include <cstddef>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto unknown_value = std::vector<std::nullptr_t>{};
process(unknown_value);
    return 0;
}
