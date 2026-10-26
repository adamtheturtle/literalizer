#include <map>
#include <string>
#include <tuple>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, std::tuple<int, std::string, bool>>>{
    {"call", "send"},
    {"args", std::make_tuple(1, "email", true)},
};
    (void)my_data;
    return 0;
}
