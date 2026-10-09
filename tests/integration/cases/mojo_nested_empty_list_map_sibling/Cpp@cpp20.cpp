#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::vector<std::map<std::string, std::vector<std::nullptr_t>>>{
    std::map<std::string, std::vector<std::nullptr_t>>{{"values", std::vector<std::nullptr_t>{}}},
    std::map<std::string, std::vector<std::nullptr_t>>{},
};
    (void)my_data;
    return 0;
}
