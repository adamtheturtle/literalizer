#include <initializer_list>
#include <string>
#include <cstddef>
struct Record0 { int x{}; std::nullptr_t y{}; };
int main() {
auto my_data = Record0{
    1,
    nullptr,
};
    (void)my_data;
    return 0;
}
