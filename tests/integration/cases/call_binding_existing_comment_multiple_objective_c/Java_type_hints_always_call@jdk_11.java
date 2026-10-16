class Main {
static Object make_widget(Object arg0) { return null; }
    public static void main() {
Object my_data = make_widget(42);
make_widget(my_data);
my_data = make_widget(my_data); // note
// extra
make_widget(my_data);
    }
}
