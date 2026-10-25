#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<int, std::map<std::string, int>>>{
    1,
    std::map<std::string, int>{{"a", 2}},
};
    (void)my_data;
    return 0;
}
