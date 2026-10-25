#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
#include <variant>
auto process(auto...) { return 0; }
int main() {
process(std::vector<std::variant<int, std::map<std::string, std::nullptr_t>>>{1, std::map<std::string, std::nullptr_t>{}}, 42);
    return 0;
}
