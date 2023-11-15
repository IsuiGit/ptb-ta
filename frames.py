#------SCRIPT START-#
#----IMPORT SECTION-#
import random
from prettytable import PrettyTable
#-------------------#
#-----CONST SECTION-#
MSG_LEN = 4096
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
        sq_frame = PrettyTable()
        sq_frame.field_names = self.frame.header
        sq_frame.add_rows([x.node for x in self.frame.nodes])
        if len(sq_frame.get_string()) < MSG_LEN:
            sq_text_frame = '```\n{}```'.format(sq_frame.get_string())
            return sq_text_frame
        else:
            return 'Слишком много символов\nИспользуйте опцию списка'

    def __section_dataframe_output__(self):
        sec_frame = ''
        for i in self.frame.nodes:
            for j,k in zip(self.frame.header, i.node):
                sec_frame += f'{j}: {k}\n'
            sec_frame += '\n'
        if len(sec_frame) < MSG_LEN:
            return [sec_frame]
        else:
            b = len(sec_frame)//MSG_LEN
            t = len(sec_frame)%MSG_LEN
            p_sec_frame = [sec_frame[i:i+b*MSG_LEN] for i in range(0, b, MSG_LEN)]
            p_sec_frame.append(sec_frame[-t:])
            return p_sec_frame
#-------------------#
