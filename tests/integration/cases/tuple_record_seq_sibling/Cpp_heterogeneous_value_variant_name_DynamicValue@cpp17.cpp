#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::vector<int>, std::vector<std::variant<int, std::string>>>>{
    {"scores", std::vector<int>{10, 20, 30}},
    {"args", std::vector<std::variant<int, std::string>>{1, "email", "a@gmail.com", 100}},
};
    (void)my_data;
    return 0;
}
