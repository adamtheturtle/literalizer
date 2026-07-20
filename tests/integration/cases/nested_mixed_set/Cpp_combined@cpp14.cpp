#include <initializer_list>
#include <string>
#include <map>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<std::string, std::initializer_list<LiteralizerVariant<bool, int, std::string>>>>{
    {"name", "Alice"},
    {"tags", std::initializer_list<LiteralizerVariant<bool, int, std::string>>{true, 42, "apple"}},
};
(void)my_data;
my_data = std::map<std::string, LiteralizerVariant<std::string, std::initializer_list<LiteralizerVariant<bool, int, std::string>>>>{
    {"name", "Alice"},
    {"tags", std::initializer_list<LiteralizerVariant<bool, int, std::string>>{true, 42, "apple"}},
};
    (void)my_data;
    return 0;
}
