defmodule TracerType_ do
  def emit(_arg), do: nil
end
defmodule Check do
  def process(_value), do: nil
  def x do
    tracer = TracerType_
    tracer.emit(process("hello"))
    tracer.emit(process(42))
    tracer.emit(process(true))
  end
end
