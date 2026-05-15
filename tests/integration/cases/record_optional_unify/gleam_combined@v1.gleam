pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("items", GList([GDict([#("id", GInt(1))]), GDict([#("id", GInt(2)), #("count", GInt(10))]), GDict([#("id", GInt(3)), #("count", GInt(20))])])),
  ])
  let my_data = GDict([
    #("items", GList([GDict([#("id", GInt(1))]), GDict([#("id", GInt(2)), #("count", GInt(10))]), GDict([#("id", GInt(3)), #("count", GInt(20))])])),
  ])
  let _ = my_data
}
