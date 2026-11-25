defmodule Check do
  def x do
    my_data = %{
        "nil" => [[[[[[[[[nil]]]]]]]]],
        "empty" => [[[[[[[[[[]]]]]]]]]],
        "siblings" => [[[[[[[[[[4, 5]]]]]]]]]],
    }
    _ = my_data
  end
end
