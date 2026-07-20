#include <initializer_list>
#include <string>
#include <map>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<std::map<std::string, int>, int>>{
    {"a", std::map<std::string, int>{{"x", 1}}},
    {"b", 2},
};
    (void)my_data;
    return 0;
}
