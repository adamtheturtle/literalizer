#include <initializer_list>
auto make_widget(auto...) { return 0; }
int main() {
auto my_data = 'prefix ${';// payload'}' // trailing
// extra
    (void)my_data;
    return 0;
}
