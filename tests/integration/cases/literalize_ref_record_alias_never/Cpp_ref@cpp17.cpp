#include <cstddef>
struct Record0 { int x{}; std::nullptr_t y{}; };
int main() {
auto value = Record0{
    1,
    nullptr,
};
auto&& my_data = value;
    (void)my_data;
    return 0;
}
