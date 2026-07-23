#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
auto process(auto...) { return 0; }
int main() {
process(std::vector<std::variant<int, std::string>>{1, "x"});
    return 0;
}
