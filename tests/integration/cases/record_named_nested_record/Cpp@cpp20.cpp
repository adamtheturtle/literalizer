#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, std::map<std::string, std::variant<int, std::string, bool, std::vector<int>>>>>{
    {"project", "alpha"},
    {"lead_task", std::map<std::string, std::variant<int, std::string, bool, std::vector<int>>>{{"id", 100}, {"description", "first task"}, {"is_done", false}, {"blocks", std::vector<int>{102, 103}}}},
};
    (void)my_data;
    return 0;
}
