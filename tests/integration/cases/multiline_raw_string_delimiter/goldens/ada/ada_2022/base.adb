with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AStr ("custom base after empty collision: )""" & Character'Val(10) & "value"),
        AStr ("custom suffix after base collision: )"" and )x0""" & Character'Val(10) & "value"),
        AStr ("custom second suffix: )"" and )x0"" and )x00""" & Character'Val(10) & "value"),
        AStr ("long base exhaustion: )"" and )abcdefghijklmnop""" & Character'Val(10) & "value")
    ];
begin
    null;
end Main;
