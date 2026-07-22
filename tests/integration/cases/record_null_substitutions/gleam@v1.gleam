pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("missing", GInt(-1)), #("present", GInt(1))]),
    GDict([#("missing", GInt(2)), #("present", GInt(3))]),
  ])
  let _ = my_data
}
