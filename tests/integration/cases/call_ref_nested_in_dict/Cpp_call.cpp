#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
auto process(auto...) { return 0; }
int main() {
auto my_var = 42;
process(std::map<std::string, std::variant<std::map<std::string, std::string>, int>>{{"key", std::map<std::string, std::string>{{"ref", "my_var"}}}, {"count", 42}});
    return 0;
}
