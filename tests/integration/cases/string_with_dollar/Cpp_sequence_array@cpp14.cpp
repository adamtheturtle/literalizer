#include <initializer_list>
#include <string>
#include <array>
int main() {
auto my_data = std::array<std::string, 2>{
    "price $10",
    "$HOME",
};
    (void)my_data;
    return 0;
}
