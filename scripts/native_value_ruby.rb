# frozen_string_literal: true

require 'date'
require 'json'

def exact_microseconds(seconds)
  micros = seconds.to_r * 1_000_000
  # A sub-microsecond corruption must not be truncated to a valid value.
  micros.denominator == 1 ? micros.numerator.to_s : micros.to_s
end

def observe_native(value)
  case value
  when NilClass then ['null', nil]
  when TrueClass, FalseClass then ['bool', value]
  when Integer then ['int', value.to_s]
  when Float
    classification = { 1 => '+inf', -1 => '-inf' }[value.infinite?]
    ['float', value.nan? ? 'nan' : classification || [value].pack('G').unpack1('H*')]
  when String then ['string', value]
  when Time
    ['datetime', [exact_microseconds(value.to_r), exact_microseconds(value.utc_offset)]]
  when DateTime then raise TypeError, 'expected Time or Date'
  when Date then ['date', value.iso8601]
  when Array then ['sequence', value.map { |item| observe_native(item) }]
  when Hash
    ['mapping', value.map { |key, item| [observe_native(key), observe_native(item)] }]
  else
    raise TypeError, "unsupported native value: #{value.class}"
  end
end
