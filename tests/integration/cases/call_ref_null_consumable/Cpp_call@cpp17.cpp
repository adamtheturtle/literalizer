#include <initializer_list>
#include <cstddef>
#include <vector>
#include <variant>
template <typename... Args> auto consume(Args...) { return 0; }
int main() {
auto my_null = nullptr;
auto regular_null = nullptr;
consume(my_null);
consume(regular_null);
    return 0;
}
