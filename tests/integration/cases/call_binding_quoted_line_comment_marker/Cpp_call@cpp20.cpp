#include <initializer_list>
#include <string>
auto make_widget(auto...) { return 0; }
int main() {
auto my_data = make_widget("first \"quote\"\n// string body"); // note
// extra
    (void)my_data;
    return 0;
}
