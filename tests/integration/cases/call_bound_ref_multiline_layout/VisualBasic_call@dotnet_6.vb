Imports System.Collections.Generic
Module Check
    Function f(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim x = New Integer()() {
            New Integer() {
                1,
                2
            },
            New Integer() {
                3,
                4
            }
        }
        f(New Integer()()()() {
            New Integer()()() {
                x
            }
        })
    End Sub
End Module
