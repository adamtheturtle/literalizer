template <typename... Args> auto make_widget(Args...) { return 0; }
template <typename... Args> auto consume(Args...) { return 0; }
int main() {
auto my_data = make_widget(42);
consume(my_data);
my_data = make_widget(42);
consume(my_data);
    return 0;
}
