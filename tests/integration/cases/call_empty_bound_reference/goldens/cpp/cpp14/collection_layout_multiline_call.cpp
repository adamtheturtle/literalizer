#include <cstddef>
#include <vector>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
auto items = std::vector<std::nullptr_t>{};
static_cast<void>(make_widget(items));
    return 0;
}
