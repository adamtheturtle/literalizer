# frozen_string_literal: true

# Independent runtime inspection. Never infer a type from expected data.
require 'date'
require 'json'

raise 'typed observations require Ruby 3 or newer' if RUBY_VERSION.split('.').first.to_i < 3

def observe_native(value)
  case value
  when NilClass then ['null']
  when TrueClass, FalseClass then ['bool', value]
  when Integer then ['int', value.to_s]
  when Float
    payload = if value.nan?
                'nan'
              elsif value.infinite?
                value.positive? ? '+inf' : '-inf'
              else
                [value].pack('G').unpack1('H*')
              end
    ['float', payload]
  when String then ['string', value]
  when Time
    offset = value.utc_offset * 1_000_000
    raise 'offset is not integral microseconds' unless offset.denominator == 1
    raise 'instant is not integral microseconds' unless (value.to_r * 1_000_000).denominator == 1

    # Time#strftime's fractional seconds follow the UTC instant even with
    # fractional offsets. Form local wall time from exact rational arithmetic.
    wall = Time.at(value.to_r + value.utc_offset).utc
    ['datetime', wall.strftime('%Y-%m-%dT%H:%M:%S.%6N'), offset.to_i.to_s]
  when DateTime
    offset = value.offset * 86_400 * 1_000_000
    raise 'offset is not integral microseconds' unless offset.denominator == 1
    raise 'instant is not integral microseconds' unless (value.sec_fraction * 1_000_000).denominator == 1

    ['datetime', value.strftime('%Y-%m-%dT%H:%M:%S.%6N'), offset.to_i.to_s]
  when Date then ['date', value.iso8601]
  when Array then ['sequence', value.map { |item| observe_native(item) }]
  when Hash
    ['mapping', value.map { |key, item| [observe_native(key), observe_native(item)] }]
  else
    raise "unsupported native observation type: #{value.class}"
  end
end
