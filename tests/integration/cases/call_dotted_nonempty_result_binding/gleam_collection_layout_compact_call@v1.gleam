pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn thing_go(_value: a) -> Nil { Nil }

pub fn main() {
  let my_data = thing_go(GList([GInt(1)]))
  let _ = my_data
}
