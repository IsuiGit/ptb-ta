#------SCRIPT START-#
#----IMPORT SECTION-#
import random
from prettytable import PrettyTable
#-------------------#
#----HEADER SECTION-#
class Header():
    def __init__(self, header):
        self.id = hash(random.randbytes(32))
        self.header = header
        self.nodes = []
#-------------------#
#------NODE SECTION-#
class Node():
    def __init__(self, node, header):
        self.header = header
        self.node = node
#-------------------#
#--------DF SECTION-#
class SimpleDataFrame():
    def __init__(self, data):
        self.frame = self.__simple_dataframe_constructor__(data)
        self.sq_frame = None

    def __simple_dataframe_constructor__(self, data):
        header = Header(data[0])
        nodes = data[1:]
        for i in nodes[0]:
            header.nodes.append(Node(i, header.id))
        return header

    def __square_dataframe_output__(self):
        sec_frame = PrettyTable()
        sq_frame.field_names = self.frame.header
        sq_frame.add_rows([x.node for x in self.frame.nodes])
        sq_text_frame = '```\n{}```'.format(sq_frame.get_string())
        return sq_text_frame

    def __section_dataframe_output__(self):
        sec_frame = ''
        for i in self.frame.nodes:
            for j,k in zip(self.frame.header, i.node):
                sec_frame += f'{j}: {k}\n'
            sec_frame += '\n'
        return sec_frame
#-------------------#