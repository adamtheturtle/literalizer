#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::vector<int>, int>>{
    {"first", std::vector<int>{
        1,
        2,
    }},
    {"second", 3},  // About the second key.
};
    (void)my_data;
    return 0;
}
