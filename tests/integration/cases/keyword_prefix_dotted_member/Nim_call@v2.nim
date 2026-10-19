type ThingType = object
template first_value(self: ThingType; args: varargs[untyped]) = discard
var thing: ThingType
thing.first_value(1)
