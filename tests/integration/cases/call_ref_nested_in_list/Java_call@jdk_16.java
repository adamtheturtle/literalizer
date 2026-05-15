class Main {
static Object process(Object... args) { return null; }
    public static void main() {
var my_var = 42;
var my_other = 7;
process(new Object[]{my_var, 42, "static"});
process(new Object[]{my_other, 7, "label"});
    }
}
