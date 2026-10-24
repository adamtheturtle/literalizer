record Record1(int a) {}
record Record0(Record1[] items) {}
class Main {
    public static void main() {
Record0 my_data = new Record0(
    new Record1[]{
        new Record1(
            1
        )
    }
);
    }
}
