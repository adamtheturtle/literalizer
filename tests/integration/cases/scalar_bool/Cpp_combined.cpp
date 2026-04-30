#include <initializer_list>
int main() {
const auto my_data = true;
(void)my_data;
my_data = true;
    (void)my_data;
    return 0;
}
