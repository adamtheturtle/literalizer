module fval_m
  use, intrinsic :: iso_fortran_env, only: int64
  implicit none
  type :: fval_t
    integer :: t = 0
  end type fval_t
contains
  function fnull() result(v); type(fval_t) :: v; end function
  function fbool(b) result(v); logical, intent(in) :: b; type(fval_t) :: v; end function
  function fint(n) result(v); integer(kind=int64), intent(in) :: n; type(fval_t) :: v; end function
  function freal(x) result(v); real, intent(in) :: x; type(fval_t) :: v; end function
  function fstr(s) result(v); character(len=*), intent(in) :: s; type(fval_t) :: v; end function
  function flist(a) result(v); type(fval_t), intent(in) :: a(:); type(fval_t) :: v; end function
  function fmap(a) result(v); type(fval_t), intent(in) :: a(:); type(fval_t) :: v; end function
  function fset(a) result(v); type(fval_t), intent(in) :: a(:); type(fval_t) :: v; end function
  function fentry(k, u) result(v); character(len=*), intent(in) :: k; type(fval_t), intent(in) :: u; type(fval_t) :: v; end function
end module fval_m
program main
    use fval_m
    implicit none
    call emit(check(fstr('user_1'), freal(1000.0)))
    call emit(check(fstr('user_2'), freal(2000.5)))
contains
    function check(user_id, ts) result(r)
        implicit none
        type(fval_t), intent(in) :: user_id, ts
        type(fval_t) :: r
        r = fnull()
    end function check
    subroutine emit(arg)
        implicit none
        type(fval_t), intent(in) :: arg
    end subroutine emit
end program main
