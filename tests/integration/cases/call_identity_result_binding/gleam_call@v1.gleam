pub type GVal {
  GList(List(GVal))
}
pub fn thing_go(_value: a) -> Nil { Nil }

pub fn main() {
  let my_data = thing_go(GList([]))
  let _ = my_data
}
