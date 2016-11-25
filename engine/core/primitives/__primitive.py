from classes.Utils import Utils

import glob
import importlib

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class Property(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, prop, prop_value, prop_desc):
        if prop == None:
            raise Exception('incompleted primitive')
        if prop_value == None and prop_desc.get('default'):
            prop_value = value.get('default')
        if prop_value == None:
            raise Exception('could not set value for primitive %s' % prop)
        prop_value = self.convert(prop_desc['type'], prop_value, prop_desc['error'])
        if prop_desc.get('values'):
		    self.check_possible_values(prop_value,
                                       prop_desc['type'],
                                       prop_desc.get('values'))
        self.value = prop_value

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def convert(self, ptype, value, error = None):
        if type(ptype) == list: ptype = ptype[0]
        try:
            if ptype == "str":
                return str(value)
            if ptype == "int":
                return int(value)
            if ptype == "bool":
                return bool(value)
            if ptype == "float":
                return float(value)
            if ptype == "long":
                return long(value)
            if ptype == "list":
                return list(value)
        except Exception, ex:
            if error:
                raise Exception(error + " (%s)" % str(ex))
            else:
                raise Exception(ex)
        if error:
            raise Exception(error)
        else:
            raise Exception('invalid property type')

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def check_possible_values(self, value, ptype, values):
        values_list = []
        for v in values:
            values_list.append(self.convert(ptype, v))
        if value not in values_list:
            raise Exception('invalid value for property')

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class __primitive__(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, properties, all_properties = None, parent = None):
        self.parent          = parent
        self.iter_cnt        = 0
        self.rendered        = ""
        self.completed        = False
        self.library         = []
        self.primitives      = []
        self.mutation_index  = 0
        self.total_mutations = 0
        self.type            = properties.get('primitive')

        properties = properties.get('properties')
        if not properties:
            raise Exception('missing properties for primitive')

        self.transforms = properties.get('transforms')

        # Set up properties that were provided in the grammar
        for prop in properties:
            for primitive_prop in all_properties:
                if prop == primitive_prop.get('name'):
                    p = Property(prop, properties[prop], primitive_prop)
                    self[prop] = p.value
                    del p

        # Set up defaults for properties that were not included
        props_provided = self.get_properties(properties)
        for prop in all_properties:
            if prop.get('name') not in props_provided:
                p = Property(prop.get('name'), prop.get('default'), prop)
                self[prop.get('name')] = p.value
                del p

        if not self.get('name'):
            self['name'] = Utils.generate_name()

        if self.transforms:
            for transform in self.transforms:
                if transform.get('apply') == "before":
                    self.value = self.apply_transforms(self.value)

        # First item in library is the original value
        if self.get('value'): self.library.append(self.value)

        if self.get('fuzzable'):
            self.init_library()
            self.total_mutations = len(self.library)
        else:
            self.completed = True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def apply_transforms(self, value, after = False):
        if self.transforms:
            for transform in self.transforms:
                if after and transform.get('apply') == 'before': continue
                tmod = None
                try:
                    tmod = importlib.import_module("transforms." +\
                                                   transform.get('name'))
                    tmod = getattr(tmod, transform.get('name'))
                except Exception, ex:
                    raise Exception("failed to import transform '%s': %s" %\
                                    (transform.get('name'), str(ex)))
                try:
                    value = tmod.transform(value)
                except Exception, ex:
                    raise Exception("failed to execute transform '%s': %s" %\
                                    (transform.get('name'), str(ex)))
        return value

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def get_mandatories(self, all_properties):
        props = []
        for property in all_properties:
            if property.get('mandatory') and property.get('mandatory') == 1:
                props.append(property.get('name'))
        return props

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def get_properties(self, properties):
        props = []
        for property in properties:
                props.append(property)
        return props

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def getParent(self):
        return self.parent

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __len__(self):
        return len(self.primitives)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __getitem__(self, c):
        return self.primitives[c]

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __iter__(self):
        return self

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def next(self):
        if self.iter_cnt >= len(self.primitives):
            self.iter_cnt = 0
            raise StopIteration
        else:
            self.iter_cnt += 1
            return self.primitives[self.iter_cnt - 1]

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def getRoot(self):
        root = self.getParent()
        while root:
            if not root.getParent(): break
            root = root.getParent()
        if not root: root = self
        return root

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def search(self, name = None, root = None):
        if self.name == name: return self
        if self.getParent().name == name: return self.getParent()
        if not root: root = self.getRoot()
        if root.name == name: return root
        for item in root.primitives:
            if item.name == name: return item
            if len(item) > 0:
                v = self.search(name, item)
                if v != None: return v

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def reset(self):
        self.mutation_index = 0
        self.value = self.library[0]

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def mutate(self):
        if self.get('fuzzable'):
            if self.mutation_index > len(self.library) - 1:
                self.completed = True
                self.value = self.library[0]

            if self.completed == True: return

            self.value = self.library[self.mutation_index]
            self.mutation_index += 1

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        value = self.value
        if self.transforms:
            for transform in self.transforms:
                if transform.get('apply') == "after":
                    value = self.apply_transforms(value)
        return value

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def init_library(self):
        pass

