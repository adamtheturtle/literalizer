defmodule Check do
  def consume_widget(_arg_value), do: nil
  def x do
    consume_widget(MapSet.new([
        1,
        2,
    ]))
  end
end
