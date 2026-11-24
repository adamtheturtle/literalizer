with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("", AStr ("unnamed")),
        AEntry ("named", AStr ("value"))
    ];
begin
    null;
end Main;
