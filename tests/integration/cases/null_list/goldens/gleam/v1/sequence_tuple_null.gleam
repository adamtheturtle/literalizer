pub type GVal {
  GNull
  GList(List(GVal))
}

pub fn main() {
  let my_data = #(
    GNull,
    GNull,
  )
  let _ = my_data
}
