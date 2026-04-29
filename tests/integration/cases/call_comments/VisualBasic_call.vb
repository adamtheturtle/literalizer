Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        ' Test cases
        process("hello")  ' single word
        process("hello world")  ' two words
        ' trailing comment
    End Sub
End Module
