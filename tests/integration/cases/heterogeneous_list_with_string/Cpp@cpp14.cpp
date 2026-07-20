#include <initializer_list>
#include <string>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::vector<LiteralizerVariant<std::string, int>>{
    "hello",
    42,
};
    (void)my_data;
    return 0;
}
