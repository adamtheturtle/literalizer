#include <initializer_list>
#include <vector>
int main() {
const auto my_data = std::vector<int>{
    0b11110100001001000000,
    -0b10011010010,
    0b11111111,
    -0b1010,
};
    (void)my_data;
    return 0;
}
