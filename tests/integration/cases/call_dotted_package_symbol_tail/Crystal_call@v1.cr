module Fixture_call_dotted_package_symbol_tail_Crystal_call
extend self
class HelperType_; def list(a = nil); 0; end; end
helper = HelperType_.new
helper.list(a: 1);
end
