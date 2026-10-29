#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, int>>{
    {"v", "ab"},
    {"ab", 1},
};
    (void)my_data;
    return 0;
}
