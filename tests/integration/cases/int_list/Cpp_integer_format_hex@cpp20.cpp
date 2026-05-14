#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<int>{
    0x1,
    0x2,
    0x3,
};
    (void)my_data;
    return 0;
}
