#include <initializer_list>
#include <vector>
#include <type_traits>
auto make_widget(auto...) { return 0; }
auto consume(auto...) { return 0; }
int main() {
auto my_data = make_widget(42, 3);
consume(my_data, 3);
    return 0;
}
