#include <initializer_list>
#include <cstddef>
auto make_widget(auto...) { return 0; }
int main() {
auto my_data = nullptr;
my_data = make_widget(42); // note
// extra
    return 0;
}
