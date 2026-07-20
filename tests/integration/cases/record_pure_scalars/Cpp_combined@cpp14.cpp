#include <initializer_list>
#include <string>
#include <map>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<std::string, int, bool, double>>{
    {"name", "Alice"},
    {"age", 30},
    {"active", true},
    {"score", 4.5},
};
(void)my_data;
my_data = std::map<std::string, LiteralizerVariant<std::string, int, bool, double>>{
    {"name", "Alice"},
    {"age", 30},
    {"active", true},
    {"score", 4.5},
};
    (void)my_data;
    return 0;
}
