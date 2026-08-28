#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
#include <variant>
struct Record0 { int id{}; std::string label; std::vector<std::nullptr_t> tags; };
int main() {
auto my_data = std::vector{
    Record0{.id = 1, .label = "first", .tags = {}},
    Record0{.id = 2, .label = "second", .tags = {}},
    Record0{.id = 3, .label = "third", .tags = {}},
};
    (void)my_data;
    return 0;
}
