#include <cstddef>
#include <variant>
#include <vector>
struct Record0 { int x{}; };
int main() {
auto my_data = std::vector<std::variant<std::vector<std::nullptr_t>, Record0>>{
    std::vector<std::nullptr_t>{},
    Record0{.x = 1},
};
    (void)my_data;
    return 0;
}
