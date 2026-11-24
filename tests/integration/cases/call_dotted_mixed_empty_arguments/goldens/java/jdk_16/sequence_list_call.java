import java.util.List;
class Main {
static class ThingType_ { Object go(Object arg0, Object arg1, Object arg2) { return null; } }
static ThingType_ thing = new ThingType_();
    public static void main() {
thing.go(List.of(), List.of(1), List.of());
thing.go(List.of("text"), List.of(2), List.of());
thing.go(List.of(), List.of("text"), List.of());
thing.go(List.of("text"), List.of(2), List.of(3));
    }
}
