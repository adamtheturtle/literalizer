#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::nullptr_t>{
    {"value", nullptr},
};
    (void)my_data;
    return 0;
}
