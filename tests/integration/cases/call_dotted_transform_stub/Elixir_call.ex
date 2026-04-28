defmodule LogType_ do
  def emit(_arg), do: nil
end
defmodule Check do
  def process(_value), do: nil
  def x do
    log = LogType_
    log.emit(process("hello"))
    log.emit(process(42))
    log.emit(process(true))
  end
end
