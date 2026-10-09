#include <initializer_list>
#include <string>
auto make_widget(auto...) { return 0; }
int main() {
const auto my_data = make_widget("text");
    (void)my_data;
    return 0;
}
