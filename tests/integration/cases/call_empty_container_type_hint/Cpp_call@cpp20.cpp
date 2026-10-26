#include <cstddef>
#include <map>
#include <string>
#include <variant>
#include <vector>
auto process(auto...) { return 0; }
int main() {
process(std::vector<std::variant<int, std::map<std::string, std::nullptr_t>>>{1, std::map<std::string, std::nullptr_t>{}}, 42);
    return 0;
}
