auto make_widget(auto...) { return 0; }
int main() {
auto my_data = (make_widget(42) // inner
 + 1) * 3;
    (void)my_data;
    return 0;
}
