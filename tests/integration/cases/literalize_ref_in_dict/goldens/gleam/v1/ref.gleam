pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_var = GInt(1)
  let my_data = GDict([
    #("key", my_var),
  ])
  let _ = my_data
}
