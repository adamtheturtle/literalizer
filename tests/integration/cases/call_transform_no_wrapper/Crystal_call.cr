module Check
extend self
def process(value = nil); 0; end
process(value: "hello");
process(value: 42);
process(value: true);
end
