{.warning[UnusedImport]:off.}
type
  ValueKind = enum
    vkStr, vkFloat, vkBool, vkList
  Value = object
    case kind: ValueKind
    of vkStr: strVal: string
    of vkFloat: floatVal: float
    of vkBool: boolVal: bool
    of vkList: listVal: seq[Value]
type Counter = object
  calls: int
proc accept(counter: var Counter, user: string, timestamp: float64): bool =
  doAssert user == (if counter.calls == 0: "user_1" else: "user_2")
  doAssert timestamp == 100.0 + float64(counter.calls)
  inc counter.calls
  user == "user_1"
var counter: Counter
var checks = 0
proc checkResult(actual: bool, expected: seq[Value]) =
  doAssert actual == expected[0].boolVal
  doAssert expected[1].strVal == (if checks == 0: "first" else: "second")
  inc checks
checkResult(counter.accept("user_1", 100.0), @[Value(kind: vkBool, boolVal: true), Value(kind: vkStr, strVal: "first")])
checkResult(counter.accept("user_2", 101.0), @[Value(kind: vkBool, boolVal: false), Value(kind: vkStr, strVal: "second")])
doAssert counter.calls == 2 and checks == 2
