#include <initializer_list>
#include <array>
int main() {
auto my_data = std::array<bool, 3>{
    true,
    false,
    true,
};
    (void)my_data;
    return 0;
}
