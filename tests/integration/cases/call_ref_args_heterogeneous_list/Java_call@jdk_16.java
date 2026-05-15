class Main {
static Object process(Object... args) { return null; }
    public static void main() {
var my_ints = new int[]{
    1,
    2,
    3
};
var my_strings = new String[]{
    "a",
    "b"
};
var my_empty = new Object[]{};
process(my_ints, 42);
process(my_strings, 7);
process(my_empty, 99);
    }
}
