Imports System.Collections.Generic
Module Check
    Dim my_data = New String() {
        "first line" & Chr(10) & "  indented" & Chr(10) & Chr(10) & "last line",
        Chr(10) & "leading newline",
        " " & vbTab & Chr(10) & "leading whitespace",
        "trailing newline" & Chr(10),
        Chr(10) & "leading and trailing" & Chr(10),
        "quotes: """""" ''' ` and backslash: \",
        "interpolation: ${value} #{value} #@value #$value $value",
        "backslash before newline: \" & Chr(10) & "next line",
        "trailing spaces  " & Chr(10) & "next",
        "C++ empty delimiter collision: )""" & Chr(10) & "value",
        "C++ first fallback collision: )"" and )x""" & Chr(10) & "value",
        "C++ second fallback collision: )"" and )x"" and )x0""" & Chr(10) & "value",
        "Rust delimiter collision: ""#" & Chr(10) & "value",
        "Lua delimiter collision: ]]" & Chr(10) & "value",
        "Swift delimiter collision: """"""#" & Chr(10) & "value",
        "Swift interpolation collision: \#(value)" & Chr(10) & "value",
        "Ruby fallback interpolation  " & Chr(10) & "#{expression} #@instance #$global",
        "NUL followed by a digit: " & Chr(0) & "7",
        "carriage" & Chr(13) & "return"
    }
End Module
