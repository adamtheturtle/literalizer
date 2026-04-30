class Main {
static Object process(Object... args) { return null; }
    public static void main() {
var shared = 1;
var other = 2;
process(shared, 1);
process(other, 0);
process(shared, 8);
    }
}
