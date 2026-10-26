#include <array>
#include <cstddef>
int main() {
auto my_data = std::array<std::array<std::array<std::array<std::nullptr_t, 0>, 1>, 1>, 2>{
    std::array<std::array<std::array<std::nullptr_t, 0>, 1>, 1>{std::array<std::array<std::nullptr_t, 0>, 1>{std::array<std::nullptr_t, 0>{}}},
    std::array<std::array<std::array<std::nullptr_t, 0>, 1>, 1>{std::array<std::array<std::nullptr_t, 0>, 1>{std::array<std::nullptr_t, 0>{}}},
};
    (void)my_data;
    return 0;
}
