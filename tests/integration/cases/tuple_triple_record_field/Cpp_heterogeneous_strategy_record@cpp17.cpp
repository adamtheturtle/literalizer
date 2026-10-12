#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
struct Record0 { std::string call; std::vector<std::variant<int, std::string, bool>> args; };
int main() {
auto my_data = Record0{
    "send",
    {
        1,
        "email",
        true,
    },
};
    (void)my_data;
    return 0;
}
