import copy
from typing import Iterable, Callable
from numbers import Number

# FIELDS
class _generic_field():
    comment:str = ""

    fieldseperator = "\t"
    lineseperator = "\n"

    def __str__(self):
        return self.to_string()

    def to_string(self):
        raise NotImplementedError("to string method needs to be implemented!")

# BLOCKS
##genericblock:
class _generic_gromos_block:
    comment: str
    content:Iterable    #some content
    def __init__(self, name: str, used: bool, content:str=None):  # content:str,
        self.used = used
        self.name = name
        self.line_seperator = "\n"
        self.field_seperator = " \t "
        self.comment_char = "#"
        self._check_import_method(content=content)


    def __str__(self):
        return self.block_to_string()

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.content)


    def _check_import_method(self, content:str = None):
        if(not content is None):
            if (isinstance(content, list) and all([isinstance(x, str) for x in content])):
                self.read_content_from_str(content)
            elif type(content) == self.__class__:
                self.content = content
            else:
                raise Exception("Generic Block did not understand the type of content")
        else:
            self.content = []

    def read_content_from_str(self, content: str):
        if (isinstance(content, str)):
            lines = content.split("\n")
        else:
            lines = content
        self.content = []
        for field in lines:
            if (not field.strip().startswith("#") and not len(field.strip()) == 0):
                self.content.append(field.strip().split())


    def block_to_string(self) -> str:
        result = self.name + self.line_seperator
        if(isinstance(self.content, list) and len(self.content) > 0 and all([isinstance(x, str) for x in self.content])):
            result += self.field_seperator.join(self.content) + self.line_seperator
        elif(isinstance(self.content, list) and  len(self.content) > 0 and all([isinstance(x, list) and all([isinstance(y, str) for y in x]) for x in self.content])):
             result += self.line_seperator.join(map(lambda x: self.field_seperator.join(x), self.content))
        elif(isinstance(self.content, (str, Number))):
            result+= self.field_seperator+str(self.content)+self.line_seperator
        else:
            result += self.field_seperator + "EMPTY"+self.line_seperator
        result += self.line_seperator + "END" + self.line_seperator
        return result

    def get_name(self):
        return self.name


class _iterable_gromos_block(_generic_gromos_block):
    table_header = [""]
    def __init__(self, name: str, used: bool, content = None):
        self._content = []
        super().__init__(name, used, content=content)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content:Iterable):
        self._content= content

    def __getitem__(self, item: int):
        return self.content[item]

    def __len__(self):
        return len(self.content)

    def append(self, obj):
        self.content.append(obj)

    def extend(self, it:Iterable):
        self.content.extend(it)

    def block_to_string(self) -> str:
        result = self.name + self.line_seperator
        result+= "#"+self.field_seperator+self.field_seperator.join(self.table_header)+ "\n"
        for x in self.content:
            result += x.to_string()
        result += "END\n"

        return result

##GENERAL
class TIMESTEP(_generic_gromos_block):
    step: int
    t: float

    def __init__(self, t: float, step: int, subcontent=False):
        super().__init__(used=True, name="TIMESTEP")
        self.t = t
        self.step = step
        self.subcontent = subcontent

    def block_to_string(self) -> str:
        result = self.name + "\n"
        result += " \t{} \t{} \n".format(self.step, self.t)
        result += "END\n"
        return result

class TITLE(_generic_gromos_block):
    content:str
    field_seperator:str = "\t"
    line_seperator:str = "\n"
    order = [[["content"]]]

    def __init__(self, content:str, field_seperator:str="\t", line_seperator:str="\n"):
        super().__init__(used=True, name="TITLE")
        self.content = content
        self.field_seperator = field_seperator
        self.line_seperator = line_seperator

    def block_to_string(self) -> str:
        result = ""
        result += str(self.name) + "\n"#double
        result += "".join(self.content)
        if ("\t >>> Generated with python lib function_libs utilities. (riniker group)\n" not in self.content):
            result += "\n\t >>> Generated with python lib function_libs utilities. (riniker group)\n"
            result += "\t >>> line_seperator: " + repr(self.line_seperator) + "\t field_seperator: " + repr(
                self.field_seperator) +"\t comments_char: " + repr(
                self.comment_char) + "\n"
        result += "END\n"#double
        return result

class TRAJ(_iterable_gromos_block):
    content:Iterable
    def __init__(self, timestep_blocks: Iterable):
        super().__init__(used=True, name="Trajectory")
        self.content = timestep_blocks
        self.dt = 0

    def block_to_string(self) -> str:
        return self.name + " contains \t" + str(len(self.content))


