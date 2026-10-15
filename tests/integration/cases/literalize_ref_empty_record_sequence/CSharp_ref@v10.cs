record Record0(int X);
class Check {
    public static void Main() {
var EmptyItems = new Record0[] {};
var PopulatedItems = new[] {
    new Record0(1)
};
var my_data = new[] {
    EmptyItems,
    PopulatedItems
};
    _ = my_data;
    }
}
