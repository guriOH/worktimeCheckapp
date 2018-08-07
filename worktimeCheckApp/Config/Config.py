import configparser

class PropertiesReader(object):

    def __init__(self):
        self.name = "./app.properties"

    def read_properties(self,Section_Name):

        config = configparser.RawConfigParser()
        config.read(self.name)

        details_dict = dict(config.items(Section_Name))
        return details_dict


# props = PropertiesReader()
#
# dic_props = props.read_properties('DBINFO')
# #
# print(dic_props)
#
# print(dic_props.get('ui.spark.savepath'))
# print(dic_props)