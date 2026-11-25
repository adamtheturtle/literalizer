void main() {
int make_widget(T...)(T args) { return 0; }
make_widget([], [1], []);
make_widget(["text"], [2], []);
make_widget([], ["text"], []);
make_widget(["text"], [2], [3]);
}
