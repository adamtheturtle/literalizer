# frozen_string_literal: true

require 'json'

def verify_sibling_permutation(rows, key_type)
  rows.each do |row|
    next unless row.instance_of?(Hash)

    raise "expected #{key_type} keys" unless row.keys.all? { |key| key.instance_of?(key_type) }
  end

  STDOUT.write(JSON.generate('rows' => rows))
end
