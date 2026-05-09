from std.utils.variant import Variant
comptime JsonValue = Variant[String, Bool]
@fieldwise_init
struct _MgrType(Copyable, Movable):
    def run(self, operation: Dict[String, JsonValue]):
        pass
@fieldwise_init
struct _AppType(Copyable, Movable):
    var mgr: _MgrType
def main():
    var app = _AppType(_MgrType())
    app.mgr.run({"type": JsonValue(String("create")), "pr_id": JsonValue(String("pr_1")), "draft": JsonValue(True)})
    app.mgr.run({"type": JsonValue(String("create")), "pr_id": JsonValue(String("pr_2"))})
