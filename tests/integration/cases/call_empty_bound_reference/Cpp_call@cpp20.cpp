#include <initializer_list>
#include <vector>
#include <cstddef>
auto make_widget(auto...) { return 0; }
int main() {
auto items = std::vector<std::nullptr_t>{};
static_cast<void>(make_widget(items));
    return 0;
}
