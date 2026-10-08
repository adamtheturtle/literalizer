pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GInt(1)),
    #("b", GStr("x")),
    #("e", #(GInt(1), GInt(2))),
    #("f", GDict([#("g", GStr("h"))])),
  ])
  let _ = my_data
}
