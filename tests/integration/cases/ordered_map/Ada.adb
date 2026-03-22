procedure Check is
   X : A_Val := AMap'(
       AEntry ("name", AStr ("Alice")),
       AEntry ("age", AInt (30)),
       AEntry ("active", ABool (True))
   );
begin
   null;
end Check;
