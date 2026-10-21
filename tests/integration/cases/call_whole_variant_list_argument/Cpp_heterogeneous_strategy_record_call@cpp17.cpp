#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
template <typename... Args> auto f(Args...) { return 0; }
int main() {
f(std::vector<std::variant<int, std::string>>{1, "x"});
    return 0;
}
