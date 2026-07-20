#include <initializer_list>
#include <string>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::vector<LiteralizerVariant<int, double, bool, std::string>>{
    42,
    3.14,
    true,
    false,
    "hello \"world\"",
};
    (void)my_data;
    return 0;
}
