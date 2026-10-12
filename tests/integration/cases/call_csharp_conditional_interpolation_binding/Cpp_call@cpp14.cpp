#include <initializer_list>
template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
auto my_data = $"{(true ? ";// payload" : "ok")}" // trailing
// extra
    (void)my_data;
    return 0;
}
