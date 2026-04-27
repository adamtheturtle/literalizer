with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AMap'[
        AEntry ("description", AStr ("# not a comment" & Character'Val(10))),
        AEntry ("name", AStr ("foo"))
    ];
begin
    my_data := AMap'[
        AEntry ("description", AStr ("# not a comment" & Character'Val(10))),
        AEntry ("name", AStr ("foo"))
    ];
end Check;
