#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<std::map<std::string, std::string>, int>>{
    std::map<std::string, std::string>{{"$ref", "ref_x"}},
    1,
    2,
};
    (void)my_data;
    return 0;
}
