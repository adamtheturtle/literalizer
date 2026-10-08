class Main {
static Object f(Object... args) { return null; }
    public static void main() {
var x = new int[][]{
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
        x
    }
});
    }
}
