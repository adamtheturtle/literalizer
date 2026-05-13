#include <initializer_list>
auto make_widget(auto...) { return 0; }
int main() {
auto result = make_widget(42);
    (void)result;
    return 0;
}
