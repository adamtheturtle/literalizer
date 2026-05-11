pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn obj_api_client_post(_data: a) -> Nil { Nil }

pub fn main() {
  obj_api_client_post(GStr("hello"))
  obj_api_client_post(GInt(42))
  obj_api_client_post(GBool(True))
}
