class Main {
static Object f(Object arg0) { return null; }
    public static void main() {
var ref_data = new int[][]{
    new int[]{
        1,
        2
    },
    new int[]{
        3,
        4
    }
};
f(new int[][][][]{
    new int[][][]{
        ref_data
    }
});
    }
}
