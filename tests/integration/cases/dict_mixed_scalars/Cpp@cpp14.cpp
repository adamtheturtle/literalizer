#include <initializer_list>
#include <string>
#include <map>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<int, std::string>>{
    {"a", 1},
    {"b", "x"},
};
    (void)my_data;
    return 0;
}
