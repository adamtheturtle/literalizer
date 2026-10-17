#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<int, std::vector<std::vector<std::string>>>>{
    0,
    std::vector<std::vector<std::string>>{std::vector<std::string>{"plain"}},
};
    (void)my_data;
    return 0;
}
