#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<double>{
    -42,
    0,
    42,
    -1.25,
    0.0,
    1.25,
};
    (void)my_data;
    return 0;
}
