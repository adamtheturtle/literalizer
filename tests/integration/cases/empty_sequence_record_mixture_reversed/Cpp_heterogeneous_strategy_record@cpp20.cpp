#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
#include <variant>
struct Record0 { int x{}; };
int main() {
auto my_data = std::vector<std::variant<Record0, std::vector<std::nullptr_t>>>{
    Record0{.x = 1},
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
