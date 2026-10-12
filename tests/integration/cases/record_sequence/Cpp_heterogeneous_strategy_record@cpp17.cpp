#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
#include <variant>
struct Record0 { int id{}; std::string label; std::vector<std::nullptr_t> tags; };
int main() {
auto my_data = std::vector{
    Record0{1, "first", {}},
    Record0{2, "second", {}},
    Record0{3, "third", {}},
};
    (void)my_data;
    return 0;
}
