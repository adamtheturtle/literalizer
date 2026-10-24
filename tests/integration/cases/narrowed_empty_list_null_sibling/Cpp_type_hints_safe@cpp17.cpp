#include <initializer_list>
#include <cstddef>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::vector<std::nullptr_t>>{
    std::vector<std::nullptr_t>{nullptr},
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
