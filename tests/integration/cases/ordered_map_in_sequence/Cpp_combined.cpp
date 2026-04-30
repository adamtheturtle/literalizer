#include <initializer_list>
#include <string>
#include <vector>
#include <utility>
#include <variant>
int main() {
const auto my_data = std::vector<std::variant<std::vector<std::pair<std::string, int>>, std::string>>{
    std::vector<std::pair<std::string, int>>{{"a", 1}},
    "hello",
};
(void)my_data;
my_data = std::vector<std::variant<std::vector<std::pair<std::string, int>>, std::string>>{
    std::vector<std::pair<std::string, int>>{{"a", 1}},
    "hello",
};
    (void)my_data;
    return 0;
}
