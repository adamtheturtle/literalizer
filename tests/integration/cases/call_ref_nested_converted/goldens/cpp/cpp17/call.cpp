#include <string>
#include <variant>
#include <vector>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto my_var = 42;
process(std::vector<std::variant<int, std::string>>{my_var, 42, "static"});
    return 0;
}
