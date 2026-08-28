pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("flow", GList([
      GInt(1),
      // After the first element.
      GInt(2),
    ])),
    // Between the key and its value.
    #("gap", GInt(3)),
    // On the block scalar header.
    #("block", GStr("Text.\n")),
    #("nested", GList([
      GInt(1),
      GInt(1),
      // On the nested alias.
    ])),
    #("anchored", GInt(4)),
    #("alias", GInt(4)),
    // On the alias.
  ])
  let my_data = GDict([
    #("flow", GList([
      GInt(1),
      // After the first element.
      GInt(2),
    ])),
    // Between the key and its value.
    #("gap", GInt(3)),
    // On the block scalar header.
    #("block", GStr("Text.\n")),
    #("nested", GList([
      GInt(1),
      GInt(1),
      // On the nested alias.
    ])),
    #("anchored", GInt(4)),
    #("alias", GInt(4)),
    // On the alias.
  ])
  let _ = my_data
}
