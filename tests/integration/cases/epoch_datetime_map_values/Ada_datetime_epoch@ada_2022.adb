with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("within_i32", AInt (1705320000)),
        AEntry ("beyond_i32", AInt (4085195400))
    ];
begin
    null;
end Main;
