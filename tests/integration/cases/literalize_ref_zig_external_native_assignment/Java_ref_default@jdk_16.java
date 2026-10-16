class Main {
    public static void main() {
var shared = new int[]{
    1,
    2
};
var my_data = new int[]{
    0
};
_ = &my_data;
my_data = shared;
_ = &my_data;
    }
}
