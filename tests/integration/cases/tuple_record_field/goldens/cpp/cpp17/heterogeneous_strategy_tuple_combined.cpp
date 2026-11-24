#include <map>
#include <string>
#include <tuple>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, std::tuple<int, std::string, std::string, int>>>{
    {"call", "send"},
    {"args", std::make_tuple(1, "email", "a@gmail.com", 100)},
};
(void)my_data;
my_data = std::map<std::string, std::variant<std::string, std::tuple<int, std::string, std::string, int>>>{
    {"call", "send"},
    {"args", std::make_tuple(1, "email", "a@gmail.com", 100)},
};
    (void)my_data;
    return 0;
}
