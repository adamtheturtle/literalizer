#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::vector<std::map<std::string, LiteralizerVariant<std::nullptr_t, int>>>{
    std::map<std::string, LiteralizerVariant<std::nullptr_t, int>>{{"replacement", nullptr}, {"present", 1}},
    std::map<std::string, LiteralizerVariant<std::nullptr_t, int>>{{"replacement", 2}, {"present", 3}},
};
    (void)my_data;
    return 0;
}
