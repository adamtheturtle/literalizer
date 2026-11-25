#include <string>
#include <variant>
#include <vector>
auto process(auto...) { return 0; }
int main() {
process(std::vector<std::variant<std::string, int, bool>>{"hello", 42, true});
    return 0;
}
