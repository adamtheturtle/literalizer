pub type GVal {
  GNull
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("replacement", GNull), #("present", GInt(1))]),
    GDict([#("replacement", GInt(2)), #("present", GInt(3))]),
  ])
  let my_data = GList([
    GDict([#("replacement", GNull), #("present", GInt(1))]),
    GDict([#("replacement", GInt(2)), #("present", GInt(3))]),
  ])
  let _ = my_data
}
