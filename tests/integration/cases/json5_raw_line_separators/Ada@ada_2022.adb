with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("double", AStr ("a" & Character'Val(226) & Character'Val(128) & Character'Val(168) & "b")),
        AEntry ("single", AStr ("c" & Character'Val(226) & Character'Val(128) & Character'Val(169) & "d")),
        AEntry ("both", AStr ("e" & Character'Val(226) & Character'Val(128) & Character'Val(168) & "f" & Character'Val(226) & Character'Val(128) & Character'Val(169) & "g")),
        AEntry ("continued", AStr ("hi")),
        AEntry ("escaped backslash", AStr ("j\" & Character'Val(226) & Character'Val(128) & Character'Val(168) & "k"))
    ];
begin
    null;
end Main;
