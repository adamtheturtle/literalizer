#include <initializer_list>
#include <vector>
#include <cstddef>
#include <type_traits>
auto consume_widget(auto...) { return 0; }
int main() {
auto shared = 1;
auto&& my_data = shared;
consume_widget(my_data);
    return 0;
}
