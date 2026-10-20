#include <initializer_list>
#include <vector>
#include <cstddef>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
make_widget(std::vector<std::nullptr_t>{});
    return 0;
}
