class Consume_ {
    construct new() {}
    call(value) {}
}
var consume = Consume_.new()
consume.call(-2147483649)
consume.call(2147483648)
