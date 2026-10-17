#include <initializer_list>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
make_widget(1);
    return 0;
}
