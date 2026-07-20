#include <initializer_list>
#include <array>
#include <cstddef>
int main() {
auto my_data = std::array<std::nullptr_t, 0>{};
    (void)my_data;
    return 0;
}
