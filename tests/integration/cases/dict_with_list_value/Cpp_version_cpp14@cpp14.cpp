#include <initializer_list>
#include <string>
#include <map>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<std::string, std::vector<int>>>{
    {"name", "Alice"},
    {"scores", std::vector<int>{10, 20, 30}},
};
    (void)my_data;
    return 0;
}
