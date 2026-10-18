#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<double>{
    5.0e-324,
    -5.0e-324,
    1.0e-310,
};
    (void)my_data;
    return 0;
}
