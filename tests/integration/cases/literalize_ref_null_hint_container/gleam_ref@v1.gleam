pub type GVal {
  GNull
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_value = GList([
    GInt(1),
    GInt(2),
  ])
  let my_data = my_value
  let _ = my_data
}
