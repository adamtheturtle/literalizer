#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<bool, int>>{
    {"keep", true},
    {"skip", 0},
};
    (void)my_data;
    return 0;
}
