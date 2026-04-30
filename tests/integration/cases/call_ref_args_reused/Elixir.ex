defmodule Check do
  def x do
    my_data = [
        [%{"$ref" => "repeated_var"}, 1],
        [%{"$ref" => "single_var"}, 0],
        [%{"$ref" => "repeated_var"}, 8],
    ]
    _ = my_data
  end
end
