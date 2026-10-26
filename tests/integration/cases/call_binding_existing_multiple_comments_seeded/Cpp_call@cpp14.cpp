template <typename... Args> auto make_widget(Args...) { return 0; }
template <typename... Args> auto consume_widget(Args...) { return 0; }
int main() {
auto my_data = make_widget(42);
consume_widget(my_data);
my_data = make_widget(my_data); // note
// extra
consume_widget(my_data);
    return 0;
}
