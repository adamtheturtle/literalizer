class Main {
static Object make_widget(Object arg0) { return null; }
    public static void main() {
var my_data = make_widget(42);
my_data = make_widget(my_data);
make_widget(my_data);
    }
}
