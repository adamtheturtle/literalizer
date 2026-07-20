#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::vector<LiteralizerVariant<std::string, std::vector<std::nullptr_t>>>{
    "48656c6c6f",
    std::vector<std::nullptr_t>{},
};
(void)my_data;
my_data = std::vector<LiteralizerVariant<std::string, std::vector<std::nullptr_t>>>{
    "48656c6c6f",
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
