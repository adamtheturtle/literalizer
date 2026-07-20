#include <initializer_list>
#include <string>
#include <map>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<std::string, int>>{
    // Configuration
    {"name", "app"},
    // Port setting
    {"port", 3000},
};
(void)my_data;
my_data = std::map<std::string, LiteralizerVariant<std::string, int>>{
    // Configuration
    {"name", "app"},
    // Port setting
    {"port", 3000},
};
    (void)my_data;
    return 0;
}
