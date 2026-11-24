class Main {
static Object make_widget(Object arg0) { return null; }
    public static void main() {
var my_data = make_widget(42) != null ?
make_widget(42) // inner
: null; // trailing
    }
}
