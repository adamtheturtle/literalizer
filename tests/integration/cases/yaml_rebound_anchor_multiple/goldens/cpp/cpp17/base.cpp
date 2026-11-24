#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<std::variant<int, std::vector<int>>>>{
    {"a", std::vector<std::variant<int, std::vector<int>>>{1, std::vector<int>{2, 3}, 3}},
};
    (void)my_data;
    return 0;
}
