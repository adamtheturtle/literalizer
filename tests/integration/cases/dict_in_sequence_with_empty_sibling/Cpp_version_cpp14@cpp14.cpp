#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::vector<LiteralizerVariant<std::map<std::string, int>, std::vector<std::nullptr_t>>>{
    std::map<std::string, int>{{"a", 1}},
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
