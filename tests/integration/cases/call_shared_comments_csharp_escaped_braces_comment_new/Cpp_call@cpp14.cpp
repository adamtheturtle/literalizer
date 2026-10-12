#include <initializer_list>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
auto my_data = ($"{{payload}} {1://}").Length >= 0 ? make_widget(42) : make_widget(42); // trailing
// extra
    (void)my_data;
    return 0;
}
