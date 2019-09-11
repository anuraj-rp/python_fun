from os import mkdir
from os.path import exists, dirname, join
import jinja2
from textx import metamodel_from_file

this_folder = dirname(__file__)

class SimpleType(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def __str__(self):
        return self.name


def get_entity_mm():
    """
    Builds a meta-model for Entity Language
    :return: the meta-model generated
    """
    type_builtins = {
        'integer': SimpleType(None, 'integer'),
        'string': SimpleType(None, 'string')
    }
    entity_mm = metamodel_from_file(join(this_folder, 'entity.tx'),
                                         classes=[SimpleType],
                                         builtins=type_builtins)
    return entity_mm


def main(debug=False):
    #Instantiate the Entity meta-model
    this_folder = dirname(__file__)
    entity_mm = get_entity_mm()
    #Build the model
    person_model = entity_mm.model_from_file(join(this_folder,
                                             'person.ent'))

    def javatype(s):
        return{
            'integer':'int',
            'string': 'String'
        }.get(s.name, s.name)
    #Create a output folder
    srcgen_folder = join(this_folder, 'srcgen')
    if not exists(srcgen_folder):
        mkdir(srcgen_folder)

    #instantiate template engine
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder),
        trim_blocks=True,
        lstrip_blocks=True
    )

    jinja_env.filters['javatype'] = javatype

    #Load Template
    template = jinja_env.get_template('java.template')

    for entity in person_model.entities:
        with open(join(srcgen_folder,
                       "%s.java" % entity.name.capitalize()), 'w') as f:
            f.write(template.render(entity=entity))


if __name__ == "__main__":
    main()
