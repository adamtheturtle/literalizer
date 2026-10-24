defmodule Check do
  def do_thing(_x_), do: nil
  def x do
    do_thing(1)
    do_thing(2)
  end
end
