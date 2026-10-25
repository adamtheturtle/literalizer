#include <initializer_list>
#include <array>
#include <cstddef>
int main() {
auto shared = std::array<std::nullptr_t, 0>{};
auto my_data = std::array<std::array<std::nullptr_t, 0>, 2>{
    shared,
    shared,
};
    (void)my_data;
    return 0;
}
