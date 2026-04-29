pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let x = GInt(0)
  let y = GInt(0)
  let my_data = GList([
    x,
    y,
  ])
  let _ = my_data
}
