#include <initializer_list>
#include <string>
#include <map>
#include <utility>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::vector<std::pair<std::string, int>>>{
    {"a", std::vector<std::pair<std::string, int>>{{"b", 1}}},
};
    (void)my_data;
    return 0;
}
