#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<long long>{
    1,
    1099511627776,
};
(void)my_data;
my_data = std::vector<long long>{
    1,
    1099511627776,
};
    (void)my_data;
    return 0;
}
