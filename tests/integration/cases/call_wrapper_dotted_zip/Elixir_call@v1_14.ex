defmodule HelpersType_ do
  def emit(_call, _zip), do: nil
end
defmodule Check do
  def process(_value), do: nil
  def x do
    helpers = HelpersType_
    helpers.emit(process(1), 42)
  end
end
