#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<std::string, int, double, bool, std::nullptr_t>>{
    {"s", "string"},
    {"i", 1},
    {"f", 1.5},
    {"b", true},
    {"n", nullptr},
    {"d", "2024-01-15"},
    {"dt", "2024-01-15T12:00:00"},
    {"by", "48656c6c6f"},
};
(void)my_data;
my_data = std::map<std::string, LiteralizerVariant<std::string, int, double, bool, std::nullptr_t>>{
    {"s", "string"},
    {"i", 1},
    {"f", 1.5},
    {"b", true},
    {"n", nullptr},
    {"d", "2024-01-15"},
    {"dt", "2024-01-15T12:00:00"},
    {"by", "48656c6c6f"},
};
    (void)my_data;
    return 0;
}
