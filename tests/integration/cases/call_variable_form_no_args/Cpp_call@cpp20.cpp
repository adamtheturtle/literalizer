#include <initializer_list>
#include <vector>
#include <cstddef>
#include <variant>
auto make_widget(auto...) { return 0; }
int main() {
auto my_data = make_widget();
    (void)my_data;
    return 0;
}
