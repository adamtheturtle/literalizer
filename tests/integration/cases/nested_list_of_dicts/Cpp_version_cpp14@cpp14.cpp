#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::vector<std::vector<std::map<std::string, std::string>>>{
    std::vector{std::map<std::string, std::string>{{"name", "Alice"}}, std::map<std::string, std::string>{{"name", "Bob"}}},
    std::vector{std::map<std::string, std::string>{{"name", "Charlie"}}, std::map<std::string, std::string>{{"name", "Dave"}}},
};
    (void)my_data;
    return 0;
}
