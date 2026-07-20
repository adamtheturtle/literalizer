#include <initializer_list>
#include <string>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::vector<std::vector<LiteralizerVariant<std::vector<int>, std::vector<std::string>>>>{
    std::vector<LiteralizerVariant<std::vector<int>, std::vector<std::string>>>{std::vector<int>{1, 2}, std::vector<std::string>{"a", "b"}},
};
    (void)my_data;
    return 0;
}
