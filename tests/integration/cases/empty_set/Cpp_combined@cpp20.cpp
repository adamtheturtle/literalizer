#include <initializer_list>
#include <cstddef>
int main() {
auto my_data = std::initializer_list<std::nullptr_t>{};
(void)my_data;
my_data = std::initializer_list<std::nullptr_t>{};
    (void)my_data;
    return 0;
}
