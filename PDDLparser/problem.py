import itertoolsclass Problem(object):    def __init__(self, name, domain, objects, init, goal):        self._name = name        self._domain = domain        self._objects = {}        for obj in objects:            self._objects[obj.type] = self._objects.get(obj.type, [])            self._objects[obj.type].append(str(obj.value))        self._init = set(map(str, init))        self._goal = set(map(str, goal))    @property    def name(self):        return self._name    @property    def domain(self):        return self._domain    @property    def objects(self):        return self._objects.copy()    @property    def init(self):        return self._init.copy()    @property    def goal(self):        return self._goal.copy()    def __str__(self):        problem_str  = '@ Problem: {0}\n'.format(self._name)        problem_str += '>> domain: {0}\n'.format(self._domain)        problem_str += '>> objects:\n'        for type, objects in self._objects.items():            problem_str += '{0} -> {1}\n'.format(type, ', '.join(sorted(objects)))        problem_str += '>> init:\n{0}\n'.format(', '.join(sorted(self._init)))        problem_str += '>> goal:\n{0}\n'.format(', '.join(sorted(self._goal)))        return problem_str