#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<std::string, std::nullptr_t, int>>{
    {"name", "Alice"},
    {"score", nullptr},
    {"age", 30},
};
(void)my_data;
my_data = std::map<std::string, LiteralizerVariant<std::string, std::nullptr_t, int>>{
    {"name", "Alice"},
    {"score", nullptr},
    {"age", 30},
};
    (void)my_data;
    return 0;
}
