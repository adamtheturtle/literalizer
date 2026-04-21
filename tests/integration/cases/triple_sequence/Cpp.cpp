#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
void check_() {
auto my_data = std::vector<std::variant<int, std::string, bool>>{
    1,
    "hello",
    true,
};
}
