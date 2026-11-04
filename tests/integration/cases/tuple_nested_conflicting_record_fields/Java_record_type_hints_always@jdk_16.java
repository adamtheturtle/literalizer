record Record1(Object[] pair) {}
record Record0(Record1 outer) {}
class Main {
    public static void main() {
Record0[] my_data = new Record0[]{
    new Record0(new Record1(new Object[]{1, "first"})),
    new Record0(new Record1(new Object[]{false, "second"}))
};
    }
}
