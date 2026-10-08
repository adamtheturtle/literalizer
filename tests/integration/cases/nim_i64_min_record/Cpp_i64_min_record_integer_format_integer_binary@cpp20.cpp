#include <initializer_list>
#include <string>
struct Record0 { long long value{}; };
int main() {
auto my_data = Record0{
    .value = (-9223372036854775807LL - 1),
};
    (void)my_data;
    return 0;
}
