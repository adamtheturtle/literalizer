#include <initializer_list>
#include <string>
#include <vector>
#include <utility>
#include <cstddef>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::vector<std::pair<std::string, LiteralizerVariant<std::vector<std::nullptr_t>, int>>>{
    {"a", std::vector<std::nullptr_t>{}},
    {"b", 1},
};
(void)my_data;
my_data = std::vector<std::pair<std::string, LiteralizerVariant<std::vector<std::nullptr_t>, int>>>{
    {"a", std::vector<std::nullptr_t>{}},
    {"b", 1},
};
    (void)my_data;
    return 0;
}
