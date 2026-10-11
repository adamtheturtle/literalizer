#include <initializer_list>
#include <string>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
const auto my_data = make_widget("text");
    (void)my_data;
    return 0;
}
