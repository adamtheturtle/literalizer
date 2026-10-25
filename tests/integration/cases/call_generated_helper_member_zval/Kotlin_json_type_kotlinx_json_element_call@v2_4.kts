import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
class _ObjType { fun ZVal(value: Any? = null): Any? = listOf<Any?>(value) }
val obj = _ObjType()
obj.ZVal(value = Json.parseToJsonElement("1"))
