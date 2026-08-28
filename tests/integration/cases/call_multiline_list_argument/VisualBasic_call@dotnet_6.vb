Imports System.Collections.Generic
Module Check
    Function process(xs As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        process(New Integer() {
            1,
            2
        })
        process(New Integer() {
            3
        })
    End Sub
End Module
