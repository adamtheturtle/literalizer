#include <initializer_list>
#include <string>
#include <map>
#include <array>
#include <cstddef>
#include <variant>
int main() {
auto my_data = {
    std::map<std::string, std::map<std::string, std::nullptr_t>>{{"mapping", std::map<std::string, std::nullptr_t>{}}},
    std::map<std::string, std::map<std::string, std::nullptr_t>>{},
};
    (void)my_data;
    return 0;
}
