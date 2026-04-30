defmodule Check do
  def x do
    my_data = [
        %{"$ref" => "ref_x"},
        1,
        2,
    ]
    _ = my_data
  end
end
