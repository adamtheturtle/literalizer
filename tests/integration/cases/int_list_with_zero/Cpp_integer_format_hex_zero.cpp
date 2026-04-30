#include <initializer_list>
#include <vector>
int main() {
const auto my_data = std::vector<int>{
    0x0,
    0x1,
    -0x1,
};
    (void)my_data;
    return 0;
}
