#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<double>{
    0.000000001,
    -0.000000001,
};
    (void)my_data;
    return 0;
}
