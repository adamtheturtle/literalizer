defmodule Check do
  def x do
    actual = 42
    my_data = [
        %{"$ref" => 1},
        %{"$ref" => nil},
        actual,
    ]
    _ = my_data
  end
end
