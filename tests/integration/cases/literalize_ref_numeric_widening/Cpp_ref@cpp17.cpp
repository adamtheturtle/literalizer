#include <initializer_list>
#include <vector>
int main() {
auto a = 1.5;
auto b = 2.0;
auto my_data = std::vector<double>{
    a,
    b,
};
    (void)my_data;
    return 0;
}
