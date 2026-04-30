#include <initializer_list>
#include <vector>
int main() {
const auto my_data = std::vector<int>{
    0xf4240,
    -0x4d2,
    0xff,
    -0xa,
};
    (void)my_data;
    return 0;
}
