#include <initializer_list>
#include <string>
#include <vector>
#include <utility>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::vector<LiteralizerVariant<std::vector<std::pair<std::string, int>>, std::string>>{
    std::vector<std::pair<std::string, int>>{{"a", 1}},
    "hello",
};
    (void)my_data;
    return 0;
}
