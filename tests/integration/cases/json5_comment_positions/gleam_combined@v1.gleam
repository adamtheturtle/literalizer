pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    //
    // document heading
    // before the first entry
    // after the key
    // before the value
    #("counts", GList([
      // before the first item
      GInt(1),  // inline block after the comma
      // before the second item
      GInt(2),
      // trailing inside the array
    ])),  // after the nested collection
    #("more", GList([
      GInt(3),
      //
      // block heading
      // block continuation
      GInt(4),  // final inline
    ])),
    // trailing inside the object
    // after the root
    // after the document
  ])
  let _ = my_data
  let my_data = GDict([
    //
    // document heading
    // before the first entry
    // after the key
    // before the value
    #("counts", GList([
      // before the first item
      GInt(1),  // inline block after the comma
      // before the second item
      GInt(2),
      // trailing inside the array
    ])),  // after the nested collection
    #("more", GList([
      GInt(3),
      //
      // block heading
      // block continuation
      GInt(4),  // final inline
    ])),
    // trailing inside the object
    // after the root
    // after the document
  ])
  let _ = my_data
}
