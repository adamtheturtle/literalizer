#include <array>
int main() {
auto shared = std::array<int, 2>{
    1,
    2,
};
auto my_data = std::array<std::array<int, 2>, 2>{
    shared,
    shared,
};
    (void)my_data;
    return 0;
}
