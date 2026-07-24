#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
auto process(auto...) { return 0; }
int main() {
auto my_var = 42;
process(std::map<std::string, std::variant<int, std::string>>{{"key", my_var}, {"count", 42}, {"label", "example"}});
    return 0;
}
