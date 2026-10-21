#include <initializer_list>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
auto value = 1;
make_widget(value);
    return 0;
}
