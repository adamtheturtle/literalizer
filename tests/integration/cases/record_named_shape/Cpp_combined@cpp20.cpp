#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::vector<std::map<std::string, std::variant<int, std::string, bool, std::vector<int>, std::vector<std::nullptr_t>>>>{
    std::map<std::string, std::variant<int, std::string, bool, std::vector<int>, std::vector<std::nullptr_t>>>{{"id", 100}, {"description", "first task"}, {"is_done", false}, {"blocks", std::vector<int>{102, 103}}},
    std::map<std::string, std::variant<int, std::string, bool, std::vector<int>, std::vector<std::nullptr_t>>>{{"id", 101}, {"description", "second task"}, {"is_done", true}, {"blocks", std::vector<std::nullptr_t>{}}},
};
(void)my_data;
my_data = std::vector<std::map<std::string, std::variant<int, std::string, bool, std::vector<int>, std::vector<std::nullptr_t>>>>{
    std::map<std::string, std::variant<int, std::string, bool, std::vector<int>, std::vector<std::nullptr_t>>>{{"id", 100}, {"description", "first task"}, {"is_done", false}, {"blocks", std::vector<int>{102, 103}}},
    std::map<std::string, std::variant<int, std::string, bool, std::vector<int>, std::vector<std::nullptr_t>>>{{"id", 101}, {"description", "second task"}, {"is_done", true}, {"blocks", std::vector<std::nullptr_t>{}}},
};
    (void)my_data;
    return 0;
}
