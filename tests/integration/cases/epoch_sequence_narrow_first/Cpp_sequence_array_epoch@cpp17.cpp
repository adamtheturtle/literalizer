#include <initializer_list>
#include <array>
int main() {
auto my_data = std::array<long long, 2>{
    0,
    2147483648,
};
    (void)my_data;
    return 0;
}
