class Main {
static class ThingType_ { Object go(Object... args) { return null; } }
static class OuterType_ { ThingType_ thing = new ThingType_(); }
static OuterType_ outer = new OuterType_();
    public static void main() {
outer.thing.go();
    }
}
