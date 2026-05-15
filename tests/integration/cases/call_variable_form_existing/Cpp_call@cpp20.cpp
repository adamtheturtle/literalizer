#include <initializer_list>
auto make_widget(auto...) { return 0; }
int main() {
my_data = make_widget(42);
    (void)my_data;
    return 0;
}
