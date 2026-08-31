#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::vector<std::variant<int, std::string>>>{
    std::vector<int>{1, 2},
    std::vector<std::string>{"a", "b"},
};
    (void)my_data;
    return 0;
}
