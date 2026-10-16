import std.json;
void main() {
auto my_data = JSONValue([
    //
    // document heading
    // before the first entry
    // after the key
    // before the value
    "counts": JSONValue([
        // before the first item
        JSONValue(1),  // inline block after the comma
        // before the second item
        JSONValue(2),
        // trailing inside the array
    ]),  // after the nested collection
    "more": JSONValue([
        JSONValue(3),
        //
        // block heading
        // block continuation
        JSONValue(4),  // final inline
    ]),
    // trailing inside the object
    // after the root
    // after the document
]);
}
