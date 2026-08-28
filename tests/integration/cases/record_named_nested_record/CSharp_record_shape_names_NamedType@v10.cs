record NamedType(int Id, string Label, bool Enabled, int[] RelatedIds);
record Record0(string Collection, NamedType FeaturedEntry);
class Check {
    public static void Main() {
var my_data = new Record0(
    "alpha",
    new NamedType(
        100,
        "first entry",
        false,
        new int[] {
            102,
            103
        }
    )
);
    }
}
