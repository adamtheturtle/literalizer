# frozen_string_literal: true

require 'json'

def verify_option_pair(data, key_type)
  outer = data.fetch(key_type == Symbol ? :outer : 'outer')
  unless [data, outer].all? { |map| map.keys.all? { |key| key.instance_of?(key_type) } }
    raise "expected #{key_type} keys"
  end

  STDOUT.write(JSON.generate(data))
end
