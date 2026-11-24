pub type GVal {
  JInt(Int)
  JDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = JDict([
    #("quote\"backslash\\", JInt(1)),
    #("line\nbreak", JInt(2)),
    #("$(literal)${text}", JInt(3)),
    #("RStr prefix", JInt(4)),
  ])
  let _ = my_data
}
