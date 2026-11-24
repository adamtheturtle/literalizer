#include <cstddef>
struct Record0 { int x{}; std::nullptr_t y{}; };
int main() {
auto value = Record0{
    .x = 1,
    .y = nullptr,
};
auto&& my_data = value;
    (void)my_data;
    return 0;
}
