#include <initializer_list>
#include <string>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::vector<std::initializer_list<std::string>>{
    std::initializer_list<std::string>{"a", "b"},
};
    (void)my_data;
    return 0;
}
