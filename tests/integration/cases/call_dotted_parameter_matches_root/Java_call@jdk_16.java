class Main {
static class OuterType_ { Object inner(Object... args) { return null; } }
static OuterType_ outer = new OuterType_();
    public static void main() {
outer.inner(1, 2);
    }
}
