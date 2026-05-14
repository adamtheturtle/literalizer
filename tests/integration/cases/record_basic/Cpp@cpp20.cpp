#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<int, std::string, bool, std::vector<int>>>{
    {"id", 1},
    {"description", "example"},
    {"is_done", false},
    {"blocks", std::vector<int>{1, 2, 3}},
};
    (void)my_data;
    return 0;
}
