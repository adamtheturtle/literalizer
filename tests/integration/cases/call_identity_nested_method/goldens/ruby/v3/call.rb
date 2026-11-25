class ThingType; def go(*a, **kw); end; end
class OuterType; def thing; ThingType.new; end; end
outer = OuterType.new
outer.thing.go()
