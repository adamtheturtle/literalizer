#include <initializer_list>
#include <vector>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
auto my_data = make_widget();
    (void)my_data;
    return 0;
}
