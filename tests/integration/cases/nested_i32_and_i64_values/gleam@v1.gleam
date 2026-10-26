pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("values", GList([GInt(1), GInt(2147483648)])),
  ])
  let _ = my_data
}
