#include <initializer_list>
#include <vector>
#include <string>
#include <map>
#include <cstddef>
#include <variant>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto my_list = std::vector<std::nullptr_t>{};
process(std::vector<std::vector<std::map<std::string, std::map<std::string, std::string>>>>{std::vector<std::map<std::string, std::map<std::string, std::string>>>{std::map<std::string, std::map<std::string, std::string>>{{"inner", my_list}}}});
    return 0;
}
