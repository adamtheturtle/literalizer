module fval_m
  implicit none
  integer, parameter :: int64 = selected_int_kind(18)
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
    ! Test cases
    call process(fmap([fval_t :: fentry('type', fstr('create')), fentry('pr_id', fstr('pr_1'))]))  ! first case
    call process(fmap([fval_t :: fentry('type', fstr('update')), fentry('pr_id', fstr('pr_2'))]))  ! second case
    ! third case
    call process(fmap([fval_t :: fentry('type', fstr('delete')), fentry('pr_id', fstr('pr_3'))]))
contains
    subroutine process(value)
        implicit none
        type(fval_t), intent(in) :: value
    end subroutine process
end program main
