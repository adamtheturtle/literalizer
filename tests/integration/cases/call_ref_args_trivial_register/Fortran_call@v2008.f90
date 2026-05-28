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
    type(fval_t) :: my_int
    type(fval_t) :: my_bool
    type(fval_t) :: my_float
    type(fval_t) :: my_list
    my_int = fint(1_int64)
    my_bool = fbool(.true.)
    my_float = freal(3.14_real64)
    my_list = flist([fval_t :: &
        fint(1_int64), &
        fint(2_int64), &
        fint(3_int64) &
    ])
    call process(my_int, fint(42_int64))
    call process(my_bool, fint(7_int64))
    call process(my_float, fint(9_int64))
    call process(my_list, fint(1_int64))
contains
    subroutine process(value, count)
        implicit none
        type(fval_t), intent(in) :: value, count
    end subroutine process
end program main
