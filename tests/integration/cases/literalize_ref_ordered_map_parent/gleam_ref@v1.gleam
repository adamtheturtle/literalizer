pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let bound = GInt(2)
  let my_data = GDict([
    #("value", bound),
  ])
  let _ = my_data
}
