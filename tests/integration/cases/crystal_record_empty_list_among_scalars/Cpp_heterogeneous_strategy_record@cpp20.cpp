#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
#include <variant>
struct Record0 { std::vector<std::variant<int, std::vector<std::nullptr_t>>> a; };
int main() {
auto my_data = Record0{
    .a = {
        1,
        std::vector<std::nullptr_t>{},
    },
};
    (void)my_data;
    return 0;
}
