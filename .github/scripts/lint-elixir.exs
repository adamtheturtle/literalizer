paths =
  IO.read(:stdio, :eof)
  |> String.split("\0", trim: true)

# Fixtures all declare `defmodule Check`, so each iteration redefines the
# same module name. Silence the "redefining module" compiler warning and
# purge the previous bytecode between fixtures so the new definition is
# the one actually invoked.
Code.put_compiler_option(:ignore_module_conflict, true)

failed =
  Enum.reduce(paths, false, fn path, acc ->
    result =
      try do
        Code.compile_file(path)
        Check.x()
        acc
      rescue
        e ->
          IO.puts(
            :stderr,
            "FAIL #{path}:\n#{Exception.format(:error, e, __STACKTRACE__)}"
          )
          true
      catch
        kind, reason ->
          IO.puts(:stderr, "FAIL #{path}:\n#{inspect({kind, reason})}")
          true
      end

    :code.purge(Check)
    :code.delete(Check)
    result
  end)

System.halt(if failed, do: 1, else: 0)
