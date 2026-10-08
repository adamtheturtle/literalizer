#include <initializer_list>
#include <cstddef>
#include <utility>
int main() {
auto my_null = nullptr;
auto&& my_data = my_null;
    (void)my_data;
    return 0;
}
