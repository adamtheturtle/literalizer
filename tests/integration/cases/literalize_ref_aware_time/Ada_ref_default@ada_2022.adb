with A_Stub; use A_Stub;
procedure Main is
    value : A_Val := AStr ("12:30:15+02:00");
    my_data : A_Val := AMap'[
        AEntry ("x", value)
    ];
begin
    null;
end Main;
