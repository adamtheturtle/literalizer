defmodule Check do
  def x do
    my_data = [
        [%{"key" => %{"$ref" => "my_var"}, "count" => 42}],
    ]
    _ = my_data
  end
end
