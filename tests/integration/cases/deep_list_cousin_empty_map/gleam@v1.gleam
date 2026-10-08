pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("items", GList([GDict([#("inner", GDict([#("x", GInt(1))]))]), GDict([#("inner", GDict([]))])]))]),
    GDict([#("items", GList([GDict([#("inner", GDict([#("x", GInt(2))]))]), GDict([#("inner", GDict([]))])]))]),
  ])
  let _ = my_data
}
