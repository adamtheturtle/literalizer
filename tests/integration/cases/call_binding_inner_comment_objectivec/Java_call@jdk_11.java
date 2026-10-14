class Main {
static Object make_widget(Object arg0) { return null; }
    public static void main() {
var my_data = make_widget(42) ?
make_widget(42) // inner
: nil; // trailing
    }
}
