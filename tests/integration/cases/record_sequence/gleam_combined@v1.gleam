pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("id", GInt(1)), #("label", GStr("first")), #("tags", GList([]))]),
    GDict([#("id", GInt(2)), #("label", GStr("second")), #("tags", GList([]))]),
    GDict([#("id", GInt(3)), #("label", GStr("third")), #("tags", GList([]))]),
  ])
  let my_data = GList([
    GDict([#("id", GInt(1)), #("label", GStr("first")), #("tags", GList([]))]),
    GDict([#("id", GInt(2)), #("label", GStr("second")), #("tags", GList([]))]),
    GDict([#("id", GInt(3)), #("label", GStr("third")), #("tags", GList([]))]),
  ])
  let _ = my_data
}
