with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("user_name", AInt (1)),
        AEntry ("user.name", AInt (2)),
        AEntry ("user-name", AInt (3)),
        AEntry ("field_name_that_is_really_quite_long_one", AInt (4)),
        AEntry ("field_name_that_is_really_quite_long_two", AInt (5))
    ];
begin
    null;
end Main;
