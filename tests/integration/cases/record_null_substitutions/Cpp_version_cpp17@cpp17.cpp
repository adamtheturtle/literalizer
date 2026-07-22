#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::map<std::string, std::variant<std::nullptr_t, int>>>{
    std::map<std::string, std::variant<std::nullptr_t, int>>{{"missing", nullptr}, {"present", 1}},
    std::map<std::string, std::variant<std::nullptr_t, int>>{{"missing", 2}, {"present", 3}},
};
    (void)my_data;
    return 0;
}
