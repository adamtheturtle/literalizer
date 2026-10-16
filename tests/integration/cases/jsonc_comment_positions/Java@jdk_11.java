import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    //
    // document heading
    // before the first entry
    // after the key
    // before the value
    Map.entry("counts", new int[]{
        // before the first item
        1,  // inline block after the comma
        // before the second item
        2
        // trailing inside the array
    }),  // after the nested collection
    Map.entry("more", new int[]{
        3,
        //
        // block heading
        // block continuation
        4  // final inline
    })
    // trailing inside the object
    // after the root
    // after the document
);
    }
}
