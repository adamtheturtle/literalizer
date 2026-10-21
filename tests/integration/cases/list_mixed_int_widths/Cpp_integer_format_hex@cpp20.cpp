#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<long long>{
    0x1,
    0x10000000000,
};
    (void)my_data;
    return 0;
}
