with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("comma_hash", AStr ("a,#b")),
        AEntry ("comma_space_hash", AStr ("trail, # comment")),
        AEntry ("escaped_quote", AStr ("quote "" and , #")),
        AEntry ("next_line", AStr ("x" & Character'Val(194) & Character'Val(133) & "y")),
        AEntry ("line_separator", AStr ("x" & Character'Val(226) & Character'Val(128) & Character'Val(168) & "y")),
        AEntry ("paragraph_separator", AStr ("x" & Character'Val(226) & Character'Val(128) & Character'Val(169) & "y"))
    ];
begin
    null;
end Main;
