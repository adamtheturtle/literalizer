#include <initializer_list>
#include <cstddef>
void check_() {
static const auto my_data = std::initializer_list<std::nullptr_t>{};
}
