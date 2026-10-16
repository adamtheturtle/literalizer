use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        //
        // document heading
        // before the first entry
        // after the key
        // before the value
        ("counts", vec![
            // before the first item
            1,  // inline block after the comma
            // before the second item
            2,
            // trailing inside the array
        ]),  // after the nested collection
        ("more", vec![
            3,
            //
            // block heading
            // block continuation
            4,  // final inline
        ]),
        // trailing inside the object
        // after the root
        // after the document
    ]);
    let _ = &my_data;
}
