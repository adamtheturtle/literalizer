#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::vector<std::variant<int, std::string, std::vector<std::variant<int, std::string>>, std::map<std::string, std::vector<bool>>>>>{
    {"h", std::vector<std::variant<int, std::string, std::vector<std::variant<int, std::string>>, std::map<std::string, std::vector<bool>>>>{1, "a", std::vector<std::variant<int, std::string>>{2, "b"}, std::map<std::string, std::vector<bool>>{{"k", std::vector<bool>{true}}}}},
};
    (void)my_data;
    return 0;
}
