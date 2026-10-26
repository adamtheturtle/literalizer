#include <string>
#include <variant>
#include <vector>
struct Record0 { std::string call; std::vector<std::variant<int, std::string>> args; };
int main() {
auto my_data = Record0{
    "send",
    {
        1,
        "email",
    },
};
    (void)my_data;
    return 0;
}
