#include <initializer_list>
#include <string>
#include <cstddef>
#include <variant>
struct Record0 { int x{}; std::nullptr_t y{}; };
#include <utility>
int main() {
auto value = Record0{
    .x = 1,
    .y = nullptr,
};
auto&& my_data = value;
    (void)my_data;
    return 0;
}
