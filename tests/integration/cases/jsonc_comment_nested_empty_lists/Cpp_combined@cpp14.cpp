#include <initializer_list>
#include <vector>
#include <cstddef>
int main() {
auto my_data = std::vector<std::vector<std::nullptr_t>>{
    // outer heading
    // first empty
    std::vector<std::nullptr_t>{},
    // second empty
    std::vector<std::nullptr_t>{},
};
(void)my_data;
my_data = std::vector<std::vector<std::nullptr_t>>{
    // outer heading
    // first empty
    std::vector<std::nullptr_t>{},
    // second empty
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
