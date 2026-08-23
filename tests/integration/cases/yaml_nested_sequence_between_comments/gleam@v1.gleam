pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GList([
      GDict([#("item", GStr("existing"))]),
      GStr("kept"),
      // This comment trails the first pair.
    ]),
    GList([GDict([#("item", GStr("next"))]), GStr("also kept")]),
    // This comment describes the last pair.
    GList([GDict([#("item", GStr("last"))]), GStr("kept too")]),
  ])
  let _ = my_data
}
