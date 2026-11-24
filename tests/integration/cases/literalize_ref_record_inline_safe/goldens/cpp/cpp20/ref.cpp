#include <cstddef>
struct Record0 { int x{}; std::nullptr_t y{}; };
int main() {
auto my_data = Record0{
    .x = 1,
    .y = nullptr,
};
    (void)my_data;
    return 0;
}
