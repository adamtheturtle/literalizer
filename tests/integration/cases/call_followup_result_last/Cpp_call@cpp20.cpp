auto make_widget(auto...) { return 0; }
auto consume(auto...) { return 0; }
int main() {
auto my_data = make_widget(42, 3);
consume(3, my_data);
    return 0;
}
