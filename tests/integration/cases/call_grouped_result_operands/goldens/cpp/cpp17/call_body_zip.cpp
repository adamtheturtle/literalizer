template <typename... Args> auto make_widget(Args...) { return 0; }
int main() {
auto my_data = ((make_widget(42) * 3) + 1) * 2;
    (void)my_data;
    return 0;
}
