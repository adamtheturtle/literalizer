object Fixture_call_deep_dotted_method_Scala_heterogeneous_strategy_record_call {
class _ClientType { def post(data: Any = null): Any = null }
class _ApiType { val client = new _ClientType }
class _ObjType { val api = new _ApiType }
val obj = new _ObjType
obj.api.client.post(data = "hello")
obj.api.client.post(data = 42)
obj.api.client.post(data = true)
}
