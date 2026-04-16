#include <initializer_list>
#include <variant>
void check_() {
auto my_data = std::initializer_list<std::nullptr_t>{};
my_data = std::initializer_list<std::nullptr_t>{};
}
