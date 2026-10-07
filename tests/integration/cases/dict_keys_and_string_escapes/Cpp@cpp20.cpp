#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::vector<int>, std::string>>{
    {"plain", std::vector<int>{1, 2}},
    {"with-dash", "a\nb"},
};
    (void)my_data;
    return 0;
}
