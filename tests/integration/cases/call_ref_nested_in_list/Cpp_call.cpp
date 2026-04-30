#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
auto process(auto...) { return 0; }
int main() {
auto my_var = 42;
auto my_other = 7;
process(std::vector<std::variant<int, std::string>>{std::move(my_var), 42, "static"});
process(std::vector<std::variant<int, std::string>>{std::move(my_other), 7, "label"});
    return 0;
}
