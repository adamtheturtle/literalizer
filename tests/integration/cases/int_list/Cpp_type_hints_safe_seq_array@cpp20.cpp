#include <initializer_list>
#include <array>
int main() {
auto my_data = std::array<int, 3>{
    1,
    2,
    3,
};
    (void)my_data;
    return 0;
}
