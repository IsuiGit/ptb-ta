#------SCRIPT START-#
#----IMPORT SECTION-#
import random
from prettytable import PrettyTable
from fuzzywuzzy import fuzz


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
        sq_text_frame = '```\n{}```'.format(sq_frame.get_string())
        return sq_text_frame

    def __section_dataframe_output__(self, teacher_username):
        if teacher_username != None:
            sec_frame = ''
            teacher_index = self.frame.header.index("Преподаватель")

            for i in self.frame.nodes:
                current_teacher_name = i.node[teacher_index]
                token_sort_similarity = fuzz.token_sort_ratio(current_teacher_name, teacher_username)
                if token_sort_similarity >= 80:
                    for j, k in zip(self.frame.header, i.node):
                        sec_frame += f'{j}: {k}\n'
                    sec_frame += '\n'

            if not sec_frame:
                sec_frame = "Нет данных для вашего преподавателя в данной таблице."

            return sec_frame
        else:
            sec_frame = ''
            for i in self.frame.nodes:
                for j, k in zip(self.frame.header, i.node):
                    sec_frame += f'{j}: {k}\n'
                sec_frame += '\n'
            if len(sec_frame) < MSG_LEN:
                return [sec_frame]
            else:
                b = len(sec_frame) // MSG_LEN
                t = len(sec_frame) % MSG_LEN
                p_sec_frame = [sec_frame[i:i + b * MSG_LEN] for i in range(0, b, MSG_LEN)]
                p_sec_frame.append(sec_frame[-t:])
                return p_sec_frame

#-------------------#
