#include <initializer_list>
#include <vector>
#include <cstddef>
int main() {
const auto my_data = std::vector<std::nullptr_t>{};
(void)my_data;
my_data = std::vector<std::nullptr_t>{};
    (void)my_data;
    return 0;
}
