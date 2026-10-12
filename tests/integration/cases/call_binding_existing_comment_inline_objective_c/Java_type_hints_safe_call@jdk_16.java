class Main {
static Object make_widget(Object... args) { return null; }
    public static void main() {
var my_data = 42;
my_data = make_widget(my_data); // note
make_widget(my_data);
    }
}
