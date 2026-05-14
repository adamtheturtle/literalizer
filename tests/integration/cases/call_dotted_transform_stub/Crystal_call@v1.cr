module Fixture_call_dotted_transform_stub_Crystal_call
extend self
def process(value = nil); 0; end
class TracerType_; def emit(_arg = nil); 0; end; end
tracer = TracerType_.new
tracer.emit(process(value: "hello"));
tracer.emit(process(value: 42));
tracer.emit(process(value: true));
end
