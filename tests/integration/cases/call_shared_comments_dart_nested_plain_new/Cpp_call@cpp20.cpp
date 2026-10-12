#include <initializer_list>
auto make_widget(auto...) { return 0; }
int main() {
auto my_data = ("${"${"// payload"}"}").length >= 0 ? make_widget(42) : make_widget(42);
    (void)my_data;
    return 0;
}
