pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("first", GStr("Alice")), #("last", GStr("Smith"))]),
    GDict([#("first", GStr("Bob")), #("middle", GStr("Quincy"))]),
  ])
  let my_data = GList([
    GDict([#("first", GStr("Alice")), #("last", GStr("Smith"))]),
    GDict([#("first", GStr("Bob")), #("middle", GStr("Quincy"))]),
  ])
  let _ = my_data
}
