#include <initializer_list>
#include <string>
#include <map>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, std::map<std::string, std::nullptr_t>>>{
    {"label", "tag"},
    {"meta", std::map<std::string, std::nullptr_t>{}},
};
    (void)my_data;
    return 0;
}
