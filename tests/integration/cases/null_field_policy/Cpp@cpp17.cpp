#include <cstddef>
#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::nullptr_t, int>>{
    {"drop", nullptr},
    {"keep", 1},
};
    (void)my_data;
    return 0;
}
