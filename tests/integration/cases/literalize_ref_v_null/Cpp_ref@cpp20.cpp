#include <initializer_list>
#include <cstddef>
#include <utility>
int main() {
auto value = nullptr;
auto&& my_data = value;
    (void)my_data;
    return 0;
}
