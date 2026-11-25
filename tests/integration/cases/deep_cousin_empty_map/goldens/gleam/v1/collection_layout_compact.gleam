pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("outer", GDict([#("inner", GDict([#("x", GInt(1))]))]))]),
    GDict([#("outer", GDict([#("inner", GDict([]))]))]),
  ])
  let _ = my_data
}
