pub type GVal {
  GNull
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("outer", GDict([#("a", GInt(1)), #("b", GStr("x")), #("c", GNull)])),
  ])
  let _ = my_data
}
