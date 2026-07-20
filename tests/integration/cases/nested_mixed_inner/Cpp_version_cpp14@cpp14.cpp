#include <initializer_list>
#include <string>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::vector<std::vector<LiteralizerVariant<int, std::string>>>{
    std::vector<LiteralizerVariant<int, std::string>>{1, "a"},
    std::vector<LiteralizerVariant<int, std::string>>{2, "b"},
};
    (void)my_data;
    return 0;
}
