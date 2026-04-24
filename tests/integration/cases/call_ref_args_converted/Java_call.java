class Check {
static Object process(Object... args) { return null; }
    public static void check() {
var myVar = new int[]{
    1,
    2,
    3
};
var myOther = new int[]{
    4,
    5,
    6
};
process(myVar, 42);
process(myOther, 7);
    }
}
