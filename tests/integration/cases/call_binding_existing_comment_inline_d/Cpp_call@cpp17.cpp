#include <initializer_list>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
auto my_data = 42;
my_data = make_widget(42); // note
    return 0;
}
