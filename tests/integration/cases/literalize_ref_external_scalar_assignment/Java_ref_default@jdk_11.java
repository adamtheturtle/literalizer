class Main {
static Object consume_widget(Object arg0) { return null; }
    public static void main() {
var my_data = 0;
var shared = 1;
consume_widget(my_data);
my_data = shared;
consume_widget(my_data);
    }
}
