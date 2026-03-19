Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Boolean()() {
            New Boolean() {True, False},
            New Boolean() {True, True}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Boolean()() {
            New Boolean() {True, False},
            New Boolean() {True, True}
        }
    End Sub
End Module
