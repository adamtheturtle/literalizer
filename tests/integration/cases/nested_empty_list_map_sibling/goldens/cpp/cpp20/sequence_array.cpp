#include <array>
#include <cstddef>
#include <initializer_list>
#include <map>
#include <string>
int main() {
auto my_data = {
    std::map<std::string, std::array<std::nullptr_t, 0>>{{"values", std::array<std::nullptr_t, 0>{}}},
    std::map<std::string, std::array<std::nullptr_t, 0>>{},
};
    (void)my_data;
    return 0;
}
