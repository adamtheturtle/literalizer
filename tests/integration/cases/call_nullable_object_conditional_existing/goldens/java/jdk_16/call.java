class Main {
static Object make_widget(Object arg0) { return null; }
static Object consume(Object arg0) { return null; }
    public static void main() {
var my_data = make_widget(7);
consume(my_data);
my_data = make_widget(13) != null ?
make_widget(13) // inner
: null; // trailing
consume(my_data);
    }
}
