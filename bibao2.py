def html_tags(tag_name):
    def wrapper_(func):
        def wrapper(*args,**kwargs):
            content = func(*args,**kwargs)
            return "<{tag}>{content}</{tag}>".format(tag=tag_name,content=content)
        return wrapper
    return wrapper_

@html_tags('b')
def hello(name="Toby"):
    return "hello,{}".format(name)

#print(hello())

hello2 = html_tags('b')(hello)
#print(hello2("world"))

def make_printer(msg1,msg2):
    def printer():
        print(msg1,msg2)
    return printer

printer = make_printer("foo","bar")
print(printer.__closure__)
print(printer.__closure__[0].cell_contents)
print(printer.__closure__[1].cell_contents)

def test(a1):
    print(a1)

test("aa")
print(test.__closure__)
