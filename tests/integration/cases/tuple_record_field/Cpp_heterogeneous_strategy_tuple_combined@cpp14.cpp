#include <initializer_list>
#include <string>
#include <map>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
#include <tuple>
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<std::string, std::tuple<int, std::string, std::string, int>>>{
    {"call", "send"},
    {"args", std::make_tuple(1, "email", "a@gmail.com", 100)},
};
(void)my_data;
my_data = std::map<std::string, LiteralizerVariant<std::string, std::tuple<int, std::string, std::string, int>>>{
    {"call", "send"},
    {"args", std::make_tuple(1, "email", "a@gmail.com", 100)},
};
    (void)my_data;
    return 0;
}
