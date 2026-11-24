pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let existing = GInt(1)
  let my_data = GDict([
    #("nested", GList([GInt(0), existing])),
  ])
  let _ = my_data
}
