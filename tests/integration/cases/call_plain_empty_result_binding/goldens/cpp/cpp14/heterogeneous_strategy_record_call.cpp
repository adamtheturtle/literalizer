#include <cstddef>
#include <vector>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
auto my_data = make_widget(std::vector<std::nullptr_t>{});
    (void)my_data;
    return 0;
}
