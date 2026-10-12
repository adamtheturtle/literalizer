#include <initializer_list>
#include <cstddef>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
auto my_data = nullptr;
my_data = make_widget(42); // note
    return 0;
}
