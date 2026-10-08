#include <initializer_list>
#include <cstddef>
#include <vector>
#include <utility>
int main() {
auto my_value = nullptr;
auto&& my_data = my_value;
    (void)my_data;
    return 0;
}
