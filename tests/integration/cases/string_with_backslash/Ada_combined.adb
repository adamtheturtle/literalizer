with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AList'[
        AStr ("C:\path\to\file"),
        AStr ("back\\slash"),
        AStr ("hello \""world\"""),
        AStr ("path\to ""# file"),
        AStr ("trailing\"),
        AStr ("both ""quotes''' here"),
        AStr ("line1\nline2" & Character'Val(10) & "with newline")
    ];
begin
    my_data := AList'[
        AStr ("C:\path\to\file"),
        AStr ("back\\slash"),
        AStr ("hello \""world\"""),
        AStr ("path\to ""# file"),
        AStr ("trailing\"),
        AStr ("both ""quotes''' here"),
        AStr ("line1\nline2" & Character'Val(10) & "with newline")
    ];
end Check;
