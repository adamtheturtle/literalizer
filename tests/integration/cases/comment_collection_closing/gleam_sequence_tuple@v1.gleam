pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = #(
    GInt(1),
    // closing
  )
  let _ = my_data
}
