#include <initializer_list>
#include <string>
#include <vector>
#include <utility>
#include <cstddef>
#include <variant>
struct Record0 { std::vector<std::pair<std::string, int>> numbers; std::vector<std::pair<std::string, std::string>> words; std::vector<std::pair<std::string, std::vector<int>>> nested; std::vector<std::pair<std::string, std::nullptr_t>> empty; bool flag{}; std::vector<std::pair<std::string, std::vector<std::pair<std::string, int>>>> nested_maps; std::vector<std::pair<std::string, std::vector<std::pair<std::string, std::nullptr_t>>>> empty_nested_maps; };
int main() {
auto my_data = Record0{
    .numbers = {
        {"first", 1},
    },
    .words = {
        {"first", "s"},
    },
    .nested = {
        {"first", std::vector<int>{
            1,
            2,
        }},
    },
    .empty = {},
    .flag = true,
    .nested_maps = {
        {"first", std::vector<std::pair<std::string, int>>{
            {"nested", 1},
        }},
    },
    .empty_nested_maps = {
        {"first", std::vector<std::pair<std::string, std::nullptr_t>>{}},
    },
};
    (void)my_data;
    return 0;
}
