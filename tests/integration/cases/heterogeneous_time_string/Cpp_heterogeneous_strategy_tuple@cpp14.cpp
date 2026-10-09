#include <initializer_list>
#include <string>
#include <vector>
#include <tuple>
struct Record0 { std::tuple<std::string, std::string> vals; };
int main() {
auto my_data = Record0{
    std::make_tuple(
        "09:30:00",
        "hello"
    ),
};
    (void)my_data;
    return 0;
}
