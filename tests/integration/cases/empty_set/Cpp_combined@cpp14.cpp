#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<std::nullptr_t>{};
(void)my_data;
my_data = std::vector<std::nullptr_t>{};
    (void)my_data;
    return 0;
}
