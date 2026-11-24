template <typename... Args> auto consume_widget(Args...) { return 0; }
int main() {
auto shared = 1;
auto&& my_data = shared;
consume_widget(my_data);
    return 0;
}
