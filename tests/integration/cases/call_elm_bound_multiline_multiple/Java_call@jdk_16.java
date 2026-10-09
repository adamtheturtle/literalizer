class Main {
static Object f(Object... args) { return null; }
    public static void main() {
var ref_data = new int[]{
    1,
    2
};
f(new int[][]{
    ref_data
});
f(new int[][]{
    ref_data
});
    }
}
