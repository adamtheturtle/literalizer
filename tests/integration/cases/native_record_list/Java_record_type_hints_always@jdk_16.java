record Record1(int age) {}
record Record0(String name, boolean active, int count, double score, Object missing, int[] scores, Record1 child) {}
class Main {
    public static void main() {
Record0[] my_data = new Record0[]{
    new Record0("Ada", true, 1, 1.5, null, new int[]{1, 2}, new Record1(3)),
    new Record0("Bob", false, 2, 2.5, null, new int[]{4}, new Record1(5))
};
    }
}
