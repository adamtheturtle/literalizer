with A_Stub; use A_Stub;
procedure Main is
                shared : A_Val := AList'[
                    AInt (1),
                    AInt (2)
                ];
                other : A_Val := AInt (3);
                payload : A_Val := AStr (Character'Val(10) & "    shared : Val" & Character'Val(10) & "shared = RInt 99");
                my_data : A_Val := AMap'[
                    AEntry ("a", shared),
                    AEntry ("b", other),
                    AEntry ("payload", payload)
                ];
begin
    null;
end Main;
