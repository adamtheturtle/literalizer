#include <initializer_list>
int main() {
// note
const auto my_data = 42;
(void)my_data;
// note
my_data = 42;
    (void)my_data;
    return 0;
}
