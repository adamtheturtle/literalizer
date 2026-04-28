with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("key" & Character'Val(10) & "with" & Character'Val(10) & "newlines", AStr ("value1")),
        AEntry ("key" & Character'Val(9) & "with" & Character'Val(9) & "tabs", AStr ("value2")),
        AEntry ("", AStr ("value3"))
    ];
begin
    my_data := AMap'[
        AEntry ("key" & Character'Val(10) & "with" & Character'Val(10) & "newlines", AStr ("value1")),
        AEntry ("key" & Character'Val(9) & "with" & Character'Val(9) & "tabs", AStr ("value2")),
        AEntry ("", AStr ("value3"))
    ];
end Main;
