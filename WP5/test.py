count = 10
class testing:

    def myfunc():
        global count
        count = count + 1
        print(count)

a = testing
a.myfunc()
