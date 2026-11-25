defmodule Check do
  def process(_value), do: nil
  def x do
    process("Dune")  # first edition
    process("Solaris")
    process("Neuromancer")  # cyberpunk
  end
end
