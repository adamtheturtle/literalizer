#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto x = std::map<std::string, std::string>{
    {"_", "_"},
};
auto my_data = std::vector<std::variant<std::map<std::string, std::string>, int>>{
    std::move(x),
    1,
    2,
};
    (void)my_data;
    return 0;
}
