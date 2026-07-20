#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
struct Record0 { std::string call; std::vector<std::variant<int, std::string>> args; };
int main() {
auto my_data = Record0{
    .call = "send",
    .args = std::vector<std::variant<int, std::string>>{
        1,
        "email",
        "a@gmail.com",
        100,
    },
};
    (void)my_data;
    return 0;
}
