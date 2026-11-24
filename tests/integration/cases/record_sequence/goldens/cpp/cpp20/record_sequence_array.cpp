#include <vector>
#include <array>
#include <cstddef>
#include <string>
struct Record0 { int id{}; std::string label; std::array<std::nullptr_t, 0> tags{}; };
int main() {
auto my_data = std::vector{
    Record0{.id = 1, .label = "first", .tags = {}},
    Record0{.id = 2, .label = "second", .tags = {}},
    Record0{.id = 3, .label = "third", .tags = {}},
};
    (void)my_data;
    return 0;
}
