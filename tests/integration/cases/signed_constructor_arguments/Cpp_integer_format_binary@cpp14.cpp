#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<double>{
    -0b101010,
    0b0,
    0b101010,
    -1.25,
    0.0,
    1.25,
};
    (void)my_data;
    return 0;
}
