#include <initializer_list>
#include <string>
#include <map>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
struct Record0 { int a{}; std::string b; };
int main() {
auto my_data = Record0{
    1,
    "x",
};
(void)my_data;
my_data = Record0{
    1,
    "x",
};
    (void)my_data;
    return 0;
}
