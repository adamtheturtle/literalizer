class Main {
static Object make_widget(Object arg0) { return null; }
static Object consume_widget(Object arg0) { return null; }
    public static void main() {
var my_data = make_widget(42);
consume_widget(my_data);
my_data = make_widget(my_data); // note
consume_widget(my_data);
    }
}
