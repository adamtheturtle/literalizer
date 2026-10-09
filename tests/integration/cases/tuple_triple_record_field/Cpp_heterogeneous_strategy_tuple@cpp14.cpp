#include <initializer_list>
#include <string>
#include <vector>
#include <tuple>
struct Record0 { std::string call; std::tuple<int, std::string, bool> args; };
int main() {
auto my_data = Record0{
    "send",
    std::make_tuple(
        1,
        "email",
        true
    ),
};
    (void)my_data;
    return 0;
}
