pub type GVal {
  GList(List(GVal))
}
pub fn outer_thing_go() -> Nil { Nil }

pub fn main() {
  outer_thing_go()
}
