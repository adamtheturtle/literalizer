#include <initializer_list>
#include <array>
int main() {
auto my_data = std::array<int, 4>{
    1000000,
    -1234,
    255,
    -10,
};
    (void)my_data;
    return 0;
}
