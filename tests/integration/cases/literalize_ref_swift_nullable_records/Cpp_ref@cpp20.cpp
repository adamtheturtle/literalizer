#include <initializer_list>
#include <string>
#include <cstddef>
#include <variant>
struct Record1 { int x{}; std::nullptr_t y{}; };
struct Record2 { std::nullptr_t x{}; std::nullptr_t y{}; };
struct Record3 { int x{}; int y{}; };
struct Record0 { Record1 nullable; Record2 null_fields; Record3 plain; };
int main() {
auto nullable = Record1{
    .x = 1,
    .y = nullptr,
};
auto null_fields = Record2{
    .x = nullptr,
    .y = nullptr,
};
auto plain = Record3{
    .x = 1,
    .y = 2,
};
auto my_data = Record0{
    .nullable = nullable,
    .null_fields = null_fields,
    .plain = plain,
};
    (void)my_data;
    return 0;
}
