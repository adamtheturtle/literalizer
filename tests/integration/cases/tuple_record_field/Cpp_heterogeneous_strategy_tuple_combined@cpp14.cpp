#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <tuple>
struct Record0 { std::string call; std::tuple<int, std::string, std::string, int> args; };
int main() {
auto my_data = Record0{
    "send",
    std::make_tuple(
        1,
        "email",
        "a@gmail.com",
        100
    ),
};
(void)my_data;
my_data = Record0{
    "send",
    std::make_tuple(
        1,
        "email",
        "a@gmail.com",
        100
    ),
};
    (void)my_data;
    return 0;
}
