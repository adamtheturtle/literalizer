class Main {
    public static void main() {
var ref_data = new int[]{
    1,
    2
};
var my_data = new int[]{
    0
};
(void)my_data;
my_data = ref_data;
(void)my_data;
    }
}
