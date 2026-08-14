with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("explicit_string", AStr ("5")),
        AEntry ("six", AStr ("explicitly tagged key"))
    ];
begin
    null;
end Main;
