class Main {
static Object make_widget(Object arg0) { return null; }
static Object consume(Object arg0) { return null; }
    public static void main() {
Object my_data = make_widget(null);
consume(my_data);
my_data = make_widget(42);
// note
consume(my_data);
    }
}
