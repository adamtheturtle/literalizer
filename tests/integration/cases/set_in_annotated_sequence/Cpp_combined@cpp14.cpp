#include <initializer_list>
#include <vector>
#include <cstddef>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::vector<LiteralizerVariant<std::initializer_list<std::nullptr_t>, std::initializer_list<int>, std::vector<std::nullptr_t>>>{
    std::initializer_list<std::nullptr_t>{},
    std::initializer_list<int>{1, 2},
    std::vector<std::nullptr_t>{},
};
(void)my_data;
my_data = std::vector<LiteralizerVariant<std::initializer_list<std::nullptr_t>, std::initializer_list<int>, std::vector<std::nullptr_t>>>{
    std::initializer_list<std::nullptr_t>{},
    std::initializer_list<int>{1, 2},
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
