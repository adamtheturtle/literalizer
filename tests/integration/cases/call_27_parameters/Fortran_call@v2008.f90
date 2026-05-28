module fval_m
  use, intrinsic :: iso_fortran_env, only: int64, real64
  implicit none
  type :: fval_t
    integer :: t = 0
  end type fval_t
contains
  function fnull() result(v); type(fval_t) :: v; end function
  function fbool(b) result(v); logical, intent(in) :: b; type(fval_t) :: v; end function
  function fint(n) result(v); integer(kind=int64), intent(in) :: n; type(fval_t) :: v; end function
  function freal(x) result(v); real(kind=real64), intent(in) :: x; type(fval_t) :: v; end function
  function fstr(s) result(v); character(len=*), intent(in) :: s; type(fval_t) :: v; end function
  function flist(a) result(v); type(fval_t), intent(in) :: a(:); type(fval_t) :: v; end function
  function fmap(a) result(v); type(fval_t), intent(in) :: a(:); type(fval_t) :: v; end function
  function fset(a) result(v); type(fval_t), intent(in) :: a(:); type(fval_t) :: v; end function
  function fentry(k, u) result(v); character(len=*), intent(in) :: k; type(fval_t), intent(in) :: u; type(fval_t) :: v; end function
end module fval_m
program main
    use fval_m
    implicit none
    call process(fint(0_int64), fint(1_int64), fint(2_int64), fint(3_int64), fint(4_int64), fint(5_int64), fint(6_int64), fint(7_int64), fint(8_int64), fint(9_int64), fint(10_int64), fint(11_int64), fint(12_int64), fint(13_int64), fint(14_int64), fint(15_int64), fint(16_int64), fint(17_int64), fint(18_int64), fint(19_int64), fint(20_int64), fint(21_int64), fint(22_int64), fint(23_int64), fint(24_int64), fint(25_int64), fint(26_int64))
contains
    subroutine process(p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, p26)
        implicit none
        type(fval_t), intent(in) :: p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, p26
    end subroutine process
end program main
