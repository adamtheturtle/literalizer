#include <cstddef>
#include <vector>
auto make_widget(auto...) { return 0; }
int main() {
make_widget(std::vector<std::nullptr_t>{});
    return 0;
}
