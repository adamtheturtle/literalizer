#include <cstddef>
#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::map<std::string, std::variant<int, std::string, std::vector<std::nullptr_t>>>>{
    std::map<std::string, std::variant<int, std::string, std::vector<std::nullptr_t>>>{{"id", 1}, {"label", "first"}, {"tags", std::vector<std::nullptr_t>{}}},
    std::map<std::string, std::variant<int, std::string, std::vector<std::nullptr_t>>>{{"id", 2}, {"label", "second"}, {"tags", std::vector<std::nullptr_t>{}}},
    std::map<std::string, std::variant<int, std::string, std::vector<std::nullptr_t>>>{{"id", 3}, {"label", "third"}, {"tags", std::vector<std::nullptr_t>{}}},
};
(void)my_data;
my_data = std::vector<std::map<std::string, std::variant<int, std::string, std::vector<std::nullptr_t>>>>{
    std::map<std::string, std::variant<int, std::string, std::vector<std::nullptr_t>>>{{"id", 1}, {"label", "first"}, {"tags", std::vector<std::nullptr_t>{}}},
    std::map<std::string, std::variant<int, std::string, std::vector<std::nullptr_t>>>{{"id", 2}, {"label", "second"}, {"tags", std::vector<std::nullptr_t>{}}},
    std::map<std::string, std::variant<int, std::string, std::vector<std::nullptr_t>>>{{"id", 3}, {"label", "third"}, {"tags", std::vector<std::nullptr_t>{}}},
};
    (void)my_data;
    return 0;
}
