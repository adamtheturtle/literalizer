#include <vector>
#include <array>
#include <cstddef>
#include <string>
struct Record0 { int id{}; std::string label; std::array<std::nullptr_t, 0> tags{}; };
int main() {
auto my_data = std::vector{
    Record0{1, "first", {}},
    Record0{2, "second", {}},
    Record0{3, "third", {}},
};
    (void)my_data;
    return 0;
}
