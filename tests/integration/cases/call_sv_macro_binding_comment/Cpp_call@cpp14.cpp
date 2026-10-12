#include <initializer_list>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
auto my_data = (`__LINE__ > 0) ? make_widget(42) : make_widget(42); // trailing `marker
    (void)my_data;
    return 0;
}
