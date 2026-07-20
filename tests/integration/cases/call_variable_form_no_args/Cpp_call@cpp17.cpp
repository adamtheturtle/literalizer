#include <initializer_list>
#include <vector>
#include <cstddef>
#include <variant>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
auto my_data = make_widget();
    (void)my_data;
    return 0;
}
