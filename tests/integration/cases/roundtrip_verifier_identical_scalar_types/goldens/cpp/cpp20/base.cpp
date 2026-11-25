#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<std::variant<bool, int>>>{
    {"value", std::vector<std::variant<bool, int>>{true, false, 0, 1}},
};
    (void)my_data;
    return 0;
}
