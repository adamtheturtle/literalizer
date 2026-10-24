pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("scores", GList([GInt(1), GInt(2)]))]),
    GDict([#("scores", GList([GInt(3), GInt(4)]))]),
  ])
  let _ = my_data
}
