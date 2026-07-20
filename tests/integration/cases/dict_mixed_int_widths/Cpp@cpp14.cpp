#include <initializer_list>
#include <string>
#include <map>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<long long, std::string>>{
    {"a", 1},
    {"b", 3000000000},
    {"c", "x"},
};
    (void)my_data;
    return 0;
}
