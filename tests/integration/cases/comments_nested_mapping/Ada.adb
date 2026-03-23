procedure Check is
   X : A_Val := AMap'(
       AEntry ("a", AMap'(AEntry ("x", AInt (1)))),
       AEntry ("b", AInt (2))
   );
begin
   null;
end Check;
