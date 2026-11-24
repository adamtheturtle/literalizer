#include <map>
#include <string>
#include <variant>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process(std::map<std::string, std::variant<int, std::string>>{{"a", 1}, {"b", "x"}});
    return 0;
}
