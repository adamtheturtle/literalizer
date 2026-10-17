class Main {
static Object consume_widget(Object arg0) { return null; }
    public static void main() {
var ref_data = new int[]{
    1,
    2
};
var my_data = new int[]{
    0
};
consume_widget(my_data);
my_data = ref_data;
consume_widget(my_data);
    }
}
