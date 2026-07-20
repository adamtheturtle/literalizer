#include <initializer_list>
#include <string>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::vector<LiteralizerVariant<int, std::string>>{
    1,
    "email",
    "a@gmail.com",
    100,
};
(void)my_data;
my_data = std::vector<LiteralizerVariant<int, std::string>>{
    1,
    "email",
    "a@gmail.com",
    100,
};
    (void)my_data;
    return 0;
}
