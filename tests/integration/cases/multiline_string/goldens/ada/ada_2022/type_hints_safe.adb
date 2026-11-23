with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AStr ("first line" & Character'Val(10) & "  indented" & Character'Val(10) & Character'Val(10) & "last line"),
        AStr (Character'Val(10) & "leading newline"),
        AStr (" " & Character'Val(9) & Character'Val(10) & "leading whitespace"),
        AStr ("trailing newline" & Character'Val(10)),
        AStr (Character'Val(10) & "leading and trailing" & Character'Val(10)),
        AStr ("quotes: """""" ''' ` and backslash: \"),
        AStr ("interpolation: ${value} #{value} #@value #$value $value"),
        AStr ("backslash before newline: \" & Character'Val(10) & "next line"),
        AStr ("trailing spaces  " & Character'Val(10) & "next"),
        AStr ("C++ empty delimiter collision: )""" & Character'Val(10) & "value"),
        AStr ("C++ first fallback collision: )"" and )x""" & Character'Val(10) & "value"),
        AStr ("C++ second fallback collision: )"" and )x"" and )x0""" & Character'Val(10) & "value"),
        AStr ("Rust delimiter collision: ""#" & Character'Val(10) & "value"),
        AStr ("Lua delimiter collision: ]]" & Character'Val(10) & "value"),
        AStr ("Swift delimiter collision: """"""#" & Character'Val(10) & "value"),
        AStr ("Swift interpolation collision: \#(value)" & Character'Val(10) & "value"),
        AStr ("Ruby fallback interpolation  " & Character'Val(10) & "#{expression} #@instance #$global"),
        AStr ("NUL followed by a digit: " & Character'Val(0) & "7"),
        AStr ("carriage" & Character'Val(13) & "return")
    ];
begin
    null;
end Main;
