#include <initializer_list>
#include <string>
#include <map>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<int, std::string>>{
    // before
    {"answer", 42},  // inline
    {"plain", "ok"},
    // trailing
};
(void)my_data;
my_data = std::map<std::string, LiteralizerVariant<int, std::string>>{
    // before
    {"answer", 42},  // inline
    {"plain", "ok"},
    // trailing
};
    (void)my_data;
    return 0;
}
