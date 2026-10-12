#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, std::vector<std::string>, int>>{
    {"title", "report"},
    {"tags", std::vector<std::string>{"draft", "urgent", "review"}},
    {"priority", 2},
};
    (void)my_data;
    return 0;
}
