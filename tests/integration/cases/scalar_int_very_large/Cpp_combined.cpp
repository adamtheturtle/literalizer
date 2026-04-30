#include <initializer_list>
int main() {
auto my_data = 9223372036854775808ULL;
(void)my_data;
my_data = 9223372036854775808ULL;
    (void)my_data;
    return 0;
}
