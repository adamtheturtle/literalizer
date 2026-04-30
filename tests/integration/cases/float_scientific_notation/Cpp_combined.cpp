#include <initializer_list>
#include <vector>
int main() {
const auto my_data = std::vector<double>{
    0.0,
    1.0,
    1500.0,
    0.001,
};
(void)my_data;
my_data = std::vector<double>{
    0.0,
    1.0,
    1500.0,
    0.001,
};
    (void)my_data;
    return 0;
}
