#include <initializer_list>
#include <array>
int main() {
auto my_data = std::array<long long, 2>{
    999999999999999999,
    -999999999999999999,
};
    (void)my_data;
    return 0;
}
