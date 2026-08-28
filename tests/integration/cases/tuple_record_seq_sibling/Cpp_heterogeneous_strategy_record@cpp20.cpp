#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
struct Record0 { std::vector<int> scores; std::vector<std::variant<int, std::string>> args; };
int main() {
auto my_data = Record0{
    .scores = {
        10,
        20,
        30,
    },
    .args = {
        1,
        "email",
        "a@gmail.com",
        100,
    },
};
    (void)my_data;
    return 0;
}
