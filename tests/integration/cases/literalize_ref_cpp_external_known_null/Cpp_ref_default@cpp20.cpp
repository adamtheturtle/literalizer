#include <initializer_list>
#include <cstddef>
#include <utility>
int main() {
auto item = nullptr;
auto my_data = nullptr;
(void)my_data;
my_data = item;
(void)my_data;
    return 0;
}
