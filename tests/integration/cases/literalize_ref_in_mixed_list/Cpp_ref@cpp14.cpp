#include <initializer_list>
#include <string>
#include <map>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto ref_x = std::map<std::string, std::string>{
    {"_", "_"},
};
auto my_data = std::vector<LiteralizerVariant<std::map<std::string, std::string>, int>>{
    std::move(ref_x),
    1,
    2,
};
    (void)my_data;
    return 0;
}
