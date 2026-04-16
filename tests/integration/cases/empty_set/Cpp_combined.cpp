#include <initializer_list>
void check_() {
auto my_data = std::initializer_list<std::nullptr_t>{};
my_data = std::initializer_list<std::nullptr_t>{};
}
