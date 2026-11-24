#include <string>
#include <variant>
#include <vector>
template <typename... Args> auto f(Args...) { return 0; }
int main() {
f(std::vector<std::variant<int, std::string>>{1, "x"});
    return 0;
}
