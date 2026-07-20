#include <initializer_list>
#include <cstddef>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::nullptr_t>{
    nullptr,
    nullptr,
};
(void)my_data;
my_data = std::vector<std::nullptr_t>{
    nullptr,
    nullptr,
};
    (void)my_data;
    return 0;
}
