require 'date'
def process(*a); end
def emit(*a); end
emit(process(value: 1), Date.new(2024, 1, 15, Date::GREGORIAN))
