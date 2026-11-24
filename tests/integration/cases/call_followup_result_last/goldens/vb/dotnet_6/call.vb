Imports System.Collections.Generic
Module Check
    Function make_widget(first As Object, second As Object) As Object
        Return Nothing
    End Function
    Function consume(first As Object, second As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_data = make_widget(42, 3)
        consume(3, my_data)
    End Sub
End Module
