#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<std::map<std::string, int>, int>>{
    std::map<std::string, int>{{"a", 1}},
    5,
};
    (void)my_data;
    return 0;
}
