defmodule Check do
  def send(_value), do: nil
  def x do
    existing = 42
    send(existing)
  end
end
