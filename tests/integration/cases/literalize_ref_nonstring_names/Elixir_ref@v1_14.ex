defmodule Check do
  def x do
    actual = %{
        "_" => "_",
    }
    my_data = [
        %{"$ref" => 1},
        %{"$ref" => nil},
        actual,
    ]
    _ = my_data
  end
end
