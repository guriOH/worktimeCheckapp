import configparser

class PropertiesReader(object):

    def __init__(self):
        self.name = "../app.properties"
        self.main_section = 'INFO'

        # Add dummy section on top
        self.lines = [ '[%s]\n' % self.main_section ]

        with open(self.name) as f:
            self.lines.extend(f.readlines())

        # This makes sure that iterator in readfp stops
        self.lines.append('')

    def readline(self):
        return self.lines.pop(0)

    def read_properties(self):

        config = configparser.RawConfigParser()
        config.read(self.name)

        details_dict = dict(config.items(self.main_section))
        return details_dict


# props = PropertiesReader()
#
# dic_props = props.read_properties()
#
# print(dic_props)
#
# print(dic_props.get('ui.spark.savepath'))
# print(dic_props)