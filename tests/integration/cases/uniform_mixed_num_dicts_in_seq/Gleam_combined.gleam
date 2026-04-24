pub type GVal {
  GInt(Int)
  GFloat(Float)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("x", GInt(1)), #("y", GFloat(2.5))]),
    GDict([#("x", GInt(3)), #("y", GFloat(4.0))]),
  ])
  let my_data = GList([
    GDict([#("x", GInt(1)), #("y", GFloat(2.5))]),
    GDict([#("x", GInt(3)), #("y", GFloat(4.0))]),
  ])
  let _ = my_data
}
