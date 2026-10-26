#include <cstddef>
#include <variant>
#include <vector>
struct Record0 { std::vector<std::variant<int, std::vector<std::nullptr_t>>> a; };
int main() {
auto my_data = Record0{
    {
        1,
        std::vector<std::nullptr_t>{},
    },
};
    (void)my_data;
    return 0;
}
