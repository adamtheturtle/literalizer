#include <map>
#include <string>
#include <utility>
#include <vector>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto my_list = std::map<std::string, std::string>{
    {"unused", "value"},
};
process(std::vector<std::vector<std::map<std::string, std::map<std::string, std::string>>>>{std::vector<std::map<std::string, std::map<std::string, std::string>>>{std::map<std::string, std::map<std::string, std::string>>{{"inner", std::move(my_list)}}}});
    return 0;
}
