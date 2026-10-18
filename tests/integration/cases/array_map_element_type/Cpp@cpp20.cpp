#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::vector<std::map<std::string, std::vector<std::map<std::string, std::vector<std::variant<int, std::vector<std::variant<double, std::vector<std::variant<std::string, std::vector<bool>>>>>>>>>>>>{
    {"d", std::vector<std::map<std::string, std::vector<std::map<std::string, std::vector<std::variant<int, std::vector<std::variant<double, std::vector<std::variant<std::string, std::vector<bool>>>>>>>>>>>{std::map<std::string, std::vector<std::map<std::string, std::vector<std::variant<int, std::vector<std::variant<double, std::vector<std::variant<std::string, std::vector<bool>>>>>>>>>>{{"a", std::vector<std::map<std::string, std::vector<std::variant<int, std::vector<std::variant<double, std::vector<std::variant<std::string, std::vector<bool>>>>>>>>>{std::map<std::string, std::vector<std::variant<int, std::vector<std::variant<double, std::vector<std::variant<std::string, std::vector<bool>>>>>>>>{{"b", std::vector<std::variant<int, std::vector<std::variant<double, std::vector<std::variant<std::string, std::vector<bool>>>>>>>{1, std::vector<std::variant<double, std::vector<std::variant<std::string, std::vector<bool>>>>>{2.5, std::vector<std::variant<std::string, std::vector<bool>>>{"x", std::vector<bool>{true}}}}}}}}}}},
};
    (void)my_data;
    return 0;
}
