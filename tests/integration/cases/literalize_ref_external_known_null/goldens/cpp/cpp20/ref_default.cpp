auto consume_widget(auto...) { return 0; }
int main() {
auto item = nullptr;
auto my_data = nullptr;
consume_widget(my_data);
my_data = item;
consume_widget(my_data);
    return 0;
}
