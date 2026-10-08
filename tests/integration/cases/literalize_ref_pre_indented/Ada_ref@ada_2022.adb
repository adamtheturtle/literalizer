with A_Stub; use A_Stub;
procedure Main is
        shared : A_Val := AList'[
            AInt (1),
            AInt (2)
        ];
        my_data : A_Val := AMap'[
            AEntry ("a", shared)
        ];
begin
    null;
end Main;
