my_data = [
  Float::INFINITY,
  -Float::INFINITY,
  Float::NAN,
]
# Independent native value checks.
raise "special float types changed" unless my_data.size == 3 && my_data.all? { |value| value.instance_of?(Float) }
raise "special float classes changed" unless my_data[0].infinite? == 1 && my_data[1].infinite? == -1 && my_data[2].nan?
