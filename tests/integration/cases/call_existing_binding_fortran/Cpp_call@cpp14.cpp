#include <initializer_list>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
auto my_data = make_widget(0);
my_data = make_widget(1);
    return 0;
}
