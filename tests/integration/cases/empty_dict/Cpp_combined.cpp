#include <initializer_list>
#include <string>
#include <map>
#include <variant>
void check_() {
auto my_data = std::map<std::string, std::monostate>{};
my_data = std::map<std::string, std::monostate>{};
}
