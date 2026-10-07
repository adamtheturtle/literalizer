#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<std::map<std::string, int>, int>>{
    std::map<std::string, int>{{"a", 1}},
    2,
};
    (void)my_data;
    return 0;
}
