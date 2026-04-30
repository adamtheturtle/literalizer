module Fixture_call_multi_args_comments_Crystal_call
extend self
def process(ts = nil, start = nil, end = nil); 0; end
process(ts: 1, start: 0, end: 3600);  # Jan 1 1970 00:00:00 - 01:00:00
process(ts: 5, start: 0, end: 3600);  # Jan 1 1970 00:00:05 - 01:00:05
process(ts: 2, start: 0, end: 5400);  # Jan 1 1970 00:00:02 - 01:30:02
end
