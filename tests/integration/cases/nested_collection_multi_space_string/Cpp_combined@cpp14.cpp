#include <initializer_list>
#include <string>
#include <map>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::vector<std::map<std::string, LiteralizerVariant<std::string, int>>>{
    std::map<std::string, LiteralizerVariant<std::string, int>>{{"key", "hello   world"}, {"value", 1}},
};
(void)my_data;
my_data = std::vector<std::map<std::string, LiteralizerVariant<std::string, int>>>{
    std::map<std::string, LiteralizerVariant<std::string, int>>{{"key", "hello   world"}, {"value", 1}},
};
    (void)my_data;
    return 0;
}
