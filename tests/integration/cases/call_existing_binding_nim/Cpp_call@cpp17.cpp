#include <initializer_list>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
auto my_data = make_widget(0);
make_widget(my_data);
my_data = make_widget(1);
make_widget(my_data);
    return 0;
}
