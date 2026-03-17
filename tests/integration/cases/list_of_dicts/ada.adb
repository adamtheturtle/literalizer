procedure Check is
   X : Integer := AList'(
       AMap'(AEntry ("name", AStr ("Alice")), AEntry ("age", AInt (30))),
       AMap'(AEntry ("name", AStr ("Bob")), AEntry ("age", AInt (25)))
   );
begin
   null;
end Check;
