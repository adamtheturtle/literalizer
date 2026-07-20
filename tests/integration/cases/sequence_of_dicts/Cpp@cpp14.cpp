#include <initializer_list>
#include <string>
#include <map>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::vector<std::map<std::string, LiteralizerVariant<std::string, int>>>{
    std::map<std::string, LiteralizerVariant<std::string, int>>{{"name", "Alice"}, {"age", 30}},
    std::map<std::string, LiteralizerVariant<std::string, int>>{{"name", "Bob"}, {"age", 25}},
};
    (void)my_data;
    return 0;
}
