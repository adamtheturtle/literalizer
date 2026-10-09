#include <initializer_list>
#include <string>
#include <vector>
#include <tuple>
#include <cstddef>
struct Record0 { std::tuple<int, std::string> filled; std::vector<std::nullptr_t> empty; };
int main() {
auto my_data = Record0{
    std::make_tuple(
        1,
        "value"
    ),
    {},
};
    (void)my_data;
    return 0;
}
