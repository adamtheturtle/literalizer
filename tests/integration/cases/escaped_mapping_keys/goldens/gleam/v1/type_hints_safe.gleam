pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("quote\"backslash\\", GInt(1)),
    #("line\nbreak", GInt(2)),
    #("$(literal)${text}", GInt(3)),
    #("RStr prefix", GInt(4)),
  ])
  let _ = my_data
}
