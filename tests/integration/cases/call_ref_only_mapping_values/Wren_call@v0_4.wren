class Consume_ {
    construct new() {}
    call(value) {}
}
var consume = Consume_.new()
var item = 42
consume.call({"field": item})
