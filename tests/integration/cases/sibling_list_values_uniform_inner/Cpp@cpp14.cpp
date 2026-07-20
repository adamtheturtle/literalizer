#include <initializer_list>
#include <string>
#include <map>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::map<std::string, std::vector<LiteralizerVariant<int, std::vector<int>>>>{
    {"lint", std::vector<LiteralizerVariant<int, std::vector<int>>>{2, std::vector<int>{1}}},
    {"test", std::vector<LiteralizerVariant<int, std::vector<int>>>{5, std::vector<int>{7}}},
};
    (void)my_data;
    return 0;
}
