#include <cstddef>
#include <string>
struct Record1 { int a{}; std::string b; std::nullptr_t c{}; };
struct Record0 { Record1 outer; };
int main() {
auto my_data = Record0{
    {
        1,
        "x",
        nullptr,
    },
};
    (void)my_data;
    return 0;
}
