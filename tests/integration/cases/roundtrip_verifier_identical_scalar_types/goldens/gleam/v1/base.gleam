pub type GVal {
  GBool(Bool)
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("value", GList([GBool(True), GBool(False), GInt(0), GInt(1)])),
  ])
  let _ = my_data
}
