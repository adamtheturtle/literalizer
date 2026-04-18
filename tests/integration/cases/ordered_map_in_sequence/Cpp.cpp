#include <initializer_list>
#include <string>
#include <vector>
#include <utility>
#include <variant>
void check_() {
auto my_data = std::vector<std::variant<std::vector<std::pair<std::string, int>>, std::string>>{
    std::vector<std::pair<std::string, int>>{{"a", 1}},
    "hello",
};
}
