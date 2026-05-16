#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
#include <tuple>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, std::tuple<int, std::string, bool>>>{
    {"call", "send"},
    {"args", std::make_tuple(1, "email", true)},
};
    (void)my_data;
    return 0;
}
