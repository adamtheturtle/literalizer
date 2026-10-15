#include <initializer_list>
#include <string>
#include <map>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::map<std::string, std::nullptr_t>>{
    // outer heading
    // first empty
    {"a", std::map<std::string, std::nullptr_t>{}},
    // second empty
    {"b", std::map<std::string, std::nullptr_t>{}},
};
    (void)my_data;
    return 0;
}
