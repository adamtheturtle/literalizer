module Fixture_call_dotted_transform_stub_Crystal_call
extend self
def process(value = nil); 0; end
class LogType_; def emit(_arg = nil); 0; end; end
log = LogType_.new
log.emit(process(value: "hello"));
log.emit(process(value: 42));
log.emit(process(value: true));
end
