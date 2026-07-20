#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<std::vector<LiteralizerVariant<int, std::vector<std::nullptr_t>>>, std::vector<LiteralizerVariant<int, std::vector<std::string>>>>>{
    {"lint", std::vector<LiteralizerVariant<int, std::vector<std::nullptr_t>>>{2, std::vector<std::nullptr_t>{}}},
    {"test", std::vector<LiteralizerVariant<int, std::vector<std::string>>>{5, std::vector<std::string>{"compile"}}},
};
(void)my_data;
my_data = std::map<std::string, LiteralizerVariant<std::vector<LiteralizerVariant<int, std::vector<std::nullptr_t>>>, std::vector<LiteralizerVariant<int, std::vector<std::string>>>>>{
    {"lint", std::vector<LiteralizerVariant<int, std::vector<std::nullptr_t>>>{2, std::vector<std::nullptr_t>{}}},
    {"test", std::vector<LiteralizerVariant<int, std::vector<std::string>>>{5, std::vector<std::string>{"compile"}}},
};
    (void)my_data;
    return 0;
}
