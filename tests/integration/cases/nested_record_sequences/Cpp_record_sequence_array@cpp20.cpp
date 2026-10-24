#include <initializer_list>
#include <string>
#include <array>
#include <variant>
#include <vector>
struct Record0 { int a{}; };
int main() {
auto my_data = std::vector{
    std::vector{Record0{.a = 1}},
    std::vector{Record0{.a = 2}},
};
    (void)my_data;
    return 0;
}
