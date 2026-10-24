#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<double>{
    -0x2a,
    0x0,
    0x2a,
    -1.25,
    0.0,
    1.25,
};
    (void)my_data;
    return 0;
}
