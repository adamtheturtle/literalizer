#include <initializer_list>
#include <string>
#include <map>
void check_() {
auto my_data = std::map<std::string, std::nullptr_t>{};
my_data = std::map<std::string, std::nullptr_t>{};
}
