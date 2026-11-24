def process(*a); end
class HelpersType; def emit(*a, **kw); end; end
helpers = HelpersType.new
helpers.emit(process(value: 1), 42)
