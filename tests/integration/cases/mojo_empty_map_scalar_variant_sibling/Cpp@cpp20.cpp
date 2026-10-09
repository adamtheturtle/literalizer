#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::vector<std::map<std::string, std::variant<int, std::string>>>{
    std::map<std::string, std::variant<int, std::string>>{{"count", 1}, {"name", "value"}},
    std::map<std::string, std::variant<int, std::string>>{},
};
    (void)my_data;
    return 0;
}
