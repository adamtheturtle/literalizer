pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn do_thing(_x_: a) -> Nil { Nil }

pub fn main() {
  do_thing(GInt(1))
  do_thing(GInt(2))
}
