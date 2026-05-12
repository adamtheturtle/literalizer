pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("sibling_lists", GDict([
      #("numbers", GList([
        GInt(1),
        GInt(2),
      ])),
      #("strings", GList([
        GStr("x"),
        GStr("y"),
      ])),
    ])),
    #("ref_marker_present", GList([
      GStr("$keep"),
      GStr("z"),
    ])),
  ])
  let _ = my_data
}
