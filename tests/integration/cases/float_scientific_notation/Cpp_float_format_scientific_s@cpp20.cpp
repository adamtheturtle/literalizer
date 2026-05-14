#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<double>{
    0.0,
    1.0,
    1.5e3,
    1.0e-3,
};
    (void)my_data;
    return 0;
}
