#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::map<std::string, std::variant<int, std::string>>>{
    std::map<std::string, std::variant<int, std::string>>{{"count", 1}, {"name", "value"}},
    std::map<std::string, std::variant<int, std::string>>{},
};
    (void)my_data;
    return 0;
}
