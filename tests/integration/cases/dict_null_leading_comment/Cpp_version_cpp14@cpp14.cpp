#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<std::string, std::nullptr_t>>{
    // comment
    {"name", "Alice"},
    {"score", nullptr},
};
    (void)my_data;
    return 0;
}
