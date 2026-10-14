#include <initializer_list>
#include <cstddef>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
auto my_data = make_widget(nullptr);
my_data = ($"{$"{1:;//}"}").Length >= 0 ? make_widget(42) : make_widget(42) // trailing
// extra
    return 0;
}
