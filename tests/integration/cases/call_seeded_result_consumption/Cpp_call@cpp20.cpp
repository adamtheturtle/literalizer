auto make_widget(auto...) { return 0; }
auto consume_widget(auto...) { return 0; }
int main() {
auto my_data = make_widget(0);
consume_widget(my_data);
my_data = make_widget(1);
consume_widget(my_data);
    return 0;
}
