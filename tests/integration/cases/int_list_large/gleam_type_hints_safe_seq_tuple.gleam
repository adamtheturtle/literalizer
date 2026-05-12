pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = #(
    GInt(1000000),
    GInt(-1234),
    GInt(255),
    GInt(-10),
  )
  let _ = my_data
}
