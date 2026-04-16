#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
void check_() {
auto my_data = std::vector<std::map<std::string, std::monostate>>{
    std::map<std::string, std::monostate>{},
    std::map<std::string, std::monostate>{},
};
}
