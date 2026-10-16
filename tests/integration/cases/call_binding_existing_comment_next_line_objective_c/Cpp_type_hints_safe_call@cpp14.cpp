#include <initializer_list>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
auto my_data = make_widget(42);
make_widget(my_data);
my_data = make_widget(my_data);
// note
make_widget(my_data);
    return 0;
}
