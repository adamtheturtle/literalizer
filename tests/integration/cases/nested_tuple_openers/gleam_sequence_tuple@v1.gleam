pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = #(
    #(#(#(GInt(1)))),
  )
  let _ = my_data
}
