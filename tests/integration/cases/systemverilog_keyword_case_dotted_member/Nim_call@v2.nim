type ThingType = object
template Before(self: ThingType; args: varargs[untyped]) = discard
var thing: ThingType
thing.Before(1)
