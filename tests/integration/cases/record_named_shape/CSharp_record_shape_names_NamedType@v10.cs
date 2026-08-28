record NamedType(int Id, string Label, bool Enabled, int[] RelatedIds);
class Check {
    public static void Main() {
var my_data = new[] {
    new NamedType(100, "first entry", false, new int[] {102, 103}),
    new NamedType(101, "second entry", true, new int[] {100})
};
    }
}
