#include <string>
#include <variant>
#include <vector>
struct Record0 { std::string call; std::vector<std::variant<int, std::string, bool>> args; };
int main() {
auto my_data = Record0{
    .call = "send",
    .args = {
        1,
        "email",
        true,
    },
};
    (void)my_data;
    return 0;
}
