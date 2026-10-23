#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<unsigned long long>{
    9'223'372'036'854'775'807,
    9223372036854775808ULL,
};
    (void)my_data;
    return 0;
}
