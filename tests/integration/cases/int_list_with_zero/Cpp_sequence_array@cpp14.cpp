#include <initializer_list>
#include <array>
int main() {
auto my_data = std::array<int, 3>{
    0,
    1,
    -1,
};
    (void)my_data;
    return 0;
}
