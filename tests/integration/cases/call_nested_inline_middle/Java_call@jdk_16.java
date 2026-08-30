class Main {
static Object f(Object... args) { return null; }
    public static void main() {
f(new String[][]{new String[]{"DEL", "b", "10"}, new String[]{"ADD", "a", "x"}});  // note
// next call
f(new String[][]{new String[]{"ADD", "c", "y"}});
    }
}
