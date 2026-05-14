#include <initializer_list>
#include <string>
#include <array>
int main() {
auto my_data = std::array<std::string, 1>{
    "48656c6c6f",
};
    (void)my_data;
    return 0;
}
