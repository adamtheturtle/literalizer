#include <initializer_list>
#include <vector>
int main() {
const auto my_data = std::vector<double>{
    1.1,
    -2.2,
    3.3,
};
    (void)my_data;
    return 0;
}
