#include <initializer_list>
#include <cstddef>
void check_() {
static auto my_data = std::initializer_list<std::nullptr_t>{};
}
