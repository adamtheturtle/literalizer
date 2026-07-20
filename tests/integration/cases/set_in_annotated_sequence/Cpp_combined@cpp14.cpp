#include <initializer_list>
#include <vector>
#include <cstddef>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::vector<LiteralizerVariant<std::vector<std::nullptr_t>, std::vector<int>>>{
    std::vector<std::nullptr_t>{},
    std::vector<int>{1, 2},
    std::vector<std::nullptr_t>{},
};
(void)my_data;
my_data = std::vector<LiteralizerVariant<std::vector<std::nullptr_t>, std::vector<int>>>{
    std::vector<std::nullptr_t>{},
    std::vector<int>{1, 2},
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
