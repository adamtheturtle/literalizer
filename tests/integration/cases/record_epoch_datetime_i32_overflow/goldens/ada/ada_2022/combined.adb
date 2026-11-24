with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("within_i32", AStr ("2024-01-15T12:00:00")),
        AEntry ("beyond_i32", AStr ("2099-06-15T08:30:00"))
    ];
begin
    my_data := AMap'[
        AEntry ("within_i32", AStr ("2024-01-15T12:00:00")),
        AEntry ("beyond_i32", AStr ("2099-06-15T08:30:00"))
    ];
end Main;
