#include <initializer_list>
#include <string>
#include <map>
struct Record0 { long long within_i32{}; long long beyond_i32{}; };
int main() {
auto my_data = Record0{
    .within_i32 = 1705320000,
    .beyond_i32 = 4085195400,
};
    (void)my_data;
    return 0;
}
