#include <initializer_list>
auto make_widget(auto...) { return 0; }
int main() {
auto my_data = 42;
my_data = make_widget(my_data); // note
make_widget(my_data);
    return 0;
}
