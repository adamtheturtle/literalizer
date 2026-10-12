#include <initializer_list>
auto make_widget(auto...) { return 0; }
int main() {
auto my_data = $"{{payload}} {1://}"; // trailing
// extra
    (void)my_data;
    return 0;
}
