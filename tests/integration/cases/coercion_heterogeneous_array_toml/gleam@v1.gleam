pub type GVal {
  GInt(Int)
  GFloat(Float)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("_", GList([GInt(1), GFloat(2.5), GInt(3)])),
  ])
  let _ = my_data
}
