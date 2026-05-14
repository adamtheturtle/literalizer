#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::map<std::string, std::variant<int, std::string>>>{
    std::map<std::string, std::variant<int, std::string>>{{"id", 1}, {"label", "first"}},
    std::map<std::string, std::variant<int, std::string>>{{"id", 2}, {"label", "second"}},
    std::map<std::string, std::variant<int, std::string>>{{"id", 3}, {"label", "third"}},
};
    (void)my_data;
    return 0;
}
