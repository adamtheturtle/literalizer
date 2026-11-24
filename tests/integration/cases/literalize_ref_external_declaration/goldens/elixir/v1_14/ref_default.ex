defmodule Check do
  def consume_widget(_arg_value), do: nil
  def x do
    shared = [
        1,
        2,
    ]
    my_data = shared
    consume_widget(my_data)
  end
end
