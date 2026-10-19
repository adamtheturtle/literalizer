with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AInt (1)),  -- tab	here and bidi <U+202E>after
        AEntry ("b", AInt (2))
    ];
begin
    null;
end Main;
