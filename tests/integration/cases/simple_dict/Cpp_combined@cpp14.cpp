#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<std::string, int, bool, std::nullptr_t>>{
    {"name", "Alice"},
    {"age", 30},
    {"active", true},
    {"score", nullptr},
};
(void)my_data;
my_data = std::map<std::string, LiteralizerVariant<std::string, int, bool, std::nullptr_t>>{
    {"name", "Alice"},
    {"age", 30},
    {"active", true},
    {"score", nullptr},
};
    (void)my_data;
    return 0;
}
