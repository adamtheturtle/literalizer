require 'date'
def check(*a); end
check(timestamp: Time.utc(2024, 1, 15, 10, 30, 0), date_value: Date.new(2024, 6, 1, Date::GREGORIAN))
