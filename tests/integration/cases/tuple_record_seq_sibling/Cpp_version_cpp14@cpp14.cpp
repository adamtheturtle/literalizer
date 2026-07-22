#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <tuple>
struct Record0 { std::vector<int> scores; std::tuple<int, std::string, std::string, int> args; };
int main() {
auto my_data = Record0{
    std::vector<int>{
        10,
        20,
        30,
    },
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
