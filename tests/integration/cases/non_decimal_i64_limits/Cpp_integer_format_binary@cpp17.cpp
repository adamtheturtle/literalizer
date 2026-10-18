#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<long long>{
    (-9223372036854775807LL - 1),
    -0b1,
    0b111111111111111111111111111111111111111111111111111111111111111,
};
    (void)my_data;
    return 0;
}
