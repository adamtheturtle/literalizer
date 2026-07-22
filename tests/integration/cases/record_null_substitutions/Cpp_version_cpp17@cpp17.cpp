#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <vector>
#include <utility>
#include <variant>
int main() {
auto my_data = std::vector<std::pair<std::string, std::vector<std::map<std::string, std::variant<std::nullptr_t, int>>>>>{
    {"rows", std::vector<std::map<std::string, std::variant<std::nullptr_t, int>>>{std::map<std::string, std::variant<std::nullptr_t, int>>{{"replacement", nullptr}, {"present", 1}}, std::map<std::string, std::variant<std::nullptr_t, int>>{{"replacement", 2}, {"present", 3}}}},
};
    (void)my_data;
    return 0;
}
