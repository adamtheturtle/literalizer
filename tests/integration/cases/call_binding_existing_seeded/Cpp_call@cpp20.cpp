#include <initializer_list>
auto make_widget(auto...) { return 0; }
int main() {
auto my_data = make_widget(42);
static_cast<void>(make_widget(my_data));
my_data = make_widget(my_data);
static_cast<void>(make_widget(my_data));
    return 0;
}
