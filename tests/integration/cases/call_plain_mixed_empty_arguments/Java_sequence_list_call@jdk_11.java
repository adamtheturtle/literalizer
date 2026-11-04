import java.util.List;
class Main {
static Object make_widget(Object arg0, Object arg1, Object arg2) { return null; }
    public static void main() {
make_widget(List.of(), List.of(1), List.of());
make_widget(List.of("text"), List.of(2), List.of());
make_widget(List.of(), List.of("text"), List.of());
make_widget(List.of("text"), List.of(2), List.of(3));
    }
}
