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
    1,
    nullptr,
};
auto null_fields = Record2{
    nullptr,
    nullptr,
};
auto plain = Record3{
    1,
    2,
};
auto my_data = Record0{
    nullable,
    null_fields,
    plain,
};
    (void)my_data;
    return 0;
}
