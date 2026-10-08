pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn helper_list(_a: a) -> Nil { Nil }

pub fn main() {
  helper_list(GInt(1))
}
