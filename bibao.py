# def make_printer(msg):
#     def printer():
#         print(msg)
#     return printer
# printer = make_printer("aaaa")
# printer()


def make_printer(msg):
    def printer():
        print(msg)
    return printer

a = make_printer("msg222")
a()



def tag(tname):
    def add_tag(content):
        return "<{0}>{1}</{0}>".format(tname,content)
    return add_tag

content="conn"
add_tag= tag('a')
print(add_tag("acon"))