class Consume_ {
    construct new() {}
    call(value) {}
}
var consume = Consume_.new()
var shared = 42
consume.call(shared)
