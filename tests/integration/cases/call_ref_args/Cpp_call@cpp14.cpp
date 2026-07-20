#include <initializer_list>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto my_var = std::vector<int>{
    1,
    2,
    3,
};
auto my_other = std::vector<int>{
    4,
    5,
    6,
};
process(std::move(my_var), 42);
process(std::move(my_other), 7);
    return 0;
}
