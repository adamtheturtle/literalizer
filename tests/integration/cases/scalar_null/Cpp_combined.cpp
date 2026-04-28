#include <initializer_list>
#include <cstddef>
int main() {
auto my_data = nullptr;
(void)my_data;
my_data = nullptr;
    (void)my_data;
    return 0;
}
