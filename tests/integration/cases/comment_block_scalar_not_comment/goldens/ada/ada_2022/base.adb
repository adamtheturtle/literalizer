with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("description", AStr ("# not a comment" & Character'Val(10))),
        AEntry ("name", AStr ("foo"))
    ];
begin
    null;
end Main;
