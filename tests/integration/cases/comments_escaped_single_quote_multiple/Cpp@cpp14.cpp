#include <initializer_list>
#include <string>
#include <map>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<std::string, int>>{
    {"host", "it's here"},  // a comment
    {"port", 80},  // another
};
    (void)my_data;
    return 0;
}
