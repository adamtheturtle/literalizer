#include <initializer_list>
#include <cstddef>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::vector<std::nullptr_t>{
    nullptr,
    nullptr,
};
(void)my_data;
my_data = std::vector<std::nullptr_t>{
    nullptr,
    nullptr,
};
    (void)my_data;
    return 0;
}
