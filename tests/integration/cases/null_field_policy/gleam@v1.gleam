pub type GVal {
  GNull
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("drop", GNull),
    #("keep", GInt(1)),
  ])
  let _ = my_data
}
