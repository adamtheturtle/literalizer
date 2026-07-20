#include <initializer_list>
#include <string>
#include <cstddef>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::vector<LiteralizerVariant<int, std::string, bool, std::nullptr_t>>{
    1,
    "hello",
    true,
    nullptr,
};
    (void)my_data;
    return 0;
}
