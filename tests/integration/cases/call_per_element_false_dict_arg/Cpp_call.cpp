#include <initializer_list>
#include <string>
#include <map>
#include <variant>
auto process(auto...) { return 0; }
int main() {
process(std::map<std::string, std::variant<int, std::string>>{{"a", 1}, {"b", "x"}});
    return 0;
}
