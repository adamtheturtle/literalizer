#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <variant>
struct Record1 { int a{}; std::string b; std::nullptr_t c{}; };
struct Record0 { Record1 outer; };
int main() {
auto my_data = Record0{
    .outer = Record1{
        .a = 1,
        .b = "x",
        .c = nullptr,
    },
};
    (void)my_data;
    return 0;
}
