#include <cstddef>
#include <vector>
auto make_widget(auto...) { return 0; }
int main() {
auto my_data = make_widget(std::vector<std::nullptr_t>{});
    (void)my_data;
    return 0;
}
