pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a-b", GInt(1)),
    #("two words", GInt(2)),
    #("she said \"hi\"", GInt(3)),
    #("", GInt(4)),
    #("valid_key", GInt(5)),
  ])
  let _ = my_data
}
