#include <initializer_list>
auto make_widget(auto...) { return 0; }
int main() {
auto my_data = make_widget(42);
my_data = make_widget(my_data);
    return 0;
}
