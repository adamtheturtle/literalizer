auto make_widget(auto...) { return 0; }
auto consume(auto...) { return 0; }
int main() {
auto my_data = make_widget(nullptr);
consume(my_data);
my_data = make_widget(42);
consume(my_data);
    return 0;
}
