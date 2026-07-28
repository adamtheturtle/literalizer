class Main {
static Object process(Object... args) { return null; }
    public static void main() {
var known_value = true;
var unknown_value = true;
process(known_value, new Object[]{unknown_value});
    }
}
