#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<std::string, std::nullptr_t>>{
    {"host", "localhost"},
    {"port", nullptr},  // not configured yet
};
(void)my_data;
my_data = std::map<std::string, LiteralizerVariant<std::string, std::nullptr_t>>{
    {"host", "localhost"},
    {"port", nullptr},  // not configured yet
};
    (void)my_data;
    return 0;
}
