#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::vector<LiteralizerVariant<std::vector<int>, std::vector<std::nullptr_t>, std::vector<std::string>>>{
    std::vector<int>{1, 2},
    std::vector<std::nullptr_t>{},
    std::vector<std::string>{"a", "b"},
};
(void)my_data;
my_data = std::vector<LiteralizerVariant<std::vector<int>, std::vector<std::nullptr_t>, std::vector<std::string>>>{
    std::vector<int>{1, 2},
    std::vector<std::nullptr_t>{},
    std::vector<std::string>{"a", "b"},
};
    (void)my_data;
    return 0;
}
