#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
auto f(auto...) { return 0; }
int main() {
f(std::vector<std::variant<int, std::string>>{1, "x"});
    return 0;
}
