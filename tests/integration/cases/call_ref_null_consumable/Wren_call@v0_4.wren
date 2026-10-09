class Consume_ {
    construct new() {}
    call(value) {}
}
var consume = Consume_.new()
var my_null = null
var regular_null = null
consume.call(my_null)
consume.call(regular_null)
