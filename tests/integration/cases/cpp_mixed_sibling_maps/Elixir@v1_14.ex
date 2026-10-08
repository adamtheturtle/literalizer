defmodule Check do
  def x do
    my_data = [
        [%{"a" => 1}, %{"a" => nil}, 42],
        [%{"a" => 1}, %{"a" => "s"}, 42],
        [%{"a" => 1}, %{"a" => nil}],
        [%{"a" => 1}, %{"a" => "s"}],
    ]
    _ = my_data
  end
end
