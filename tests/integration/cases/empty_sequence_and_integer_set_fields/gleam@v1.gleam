pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GDict([
    #("a", GList([])),
    #("b", GSet([GInt(1), GInt(2)])),
  ])
  let _ = my_data
}
