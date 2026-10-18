#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<long long>{
    -2147483649,
    -2147483648,
    2147483647,
    2147483648,
};
    (void)my_data;
    return 0;
}
