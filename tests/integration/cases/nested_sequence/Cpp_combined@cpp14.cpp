#include <initializer_list>
#include <string>
#include <cstddef>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::vector<LiteralizerVariant<bool, std::string, std::vector<int>, std::nullptr_t>>{
    true,
    "hi",
    std::vector<int>{1, 2},
    nullptr,
};
(void)my_data;
my_data = std::vector<LiteralizerVariant<bool, std::string, std::vector<int>, std::nullptr_t>>{
    true,
    "hi",
    std::vector<int>{1, 2},
    nullptr,
};
    (void)my_data;
    return 0;
}
