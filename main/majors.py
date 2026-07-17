import random

class Major:
    sections = []
    majors = []
    json_obj = {}

    def __init__(self, name, SAT, ACT, section, duration=4):
        self.name = name
        self.duration = duration
        self.SAT = SAT
        self.ACT = ACT
        self.section = section

        if section not in Major.sections:
            Major.sections.append(section)

        Major.majors.append(self)

        self.json = {
            "name": name,
            "duration": duration,
            "SAT": SAT,
            "ACT": ACT,
            "section": section
        }

        if section not in Major.json_obj:
            Major.json_obj[section] = []

        Major.json_obj[section].append(self.json)

    def __eq__(self, other):
        if isinstance(other, Major):
            return self.name == other.name
        raise TypeError(f"can't compare 'Major' and {other.__class__.__name__}")
    
    def __ne__(self, other):
        return not self == other
    
    @classmethod
    def get_by_section(cls, section):
        res = []
        for major in cls.majors:
            if major.section == section:
                res.append(major)

        return res


for i in range(5):
    Major(f"Major{i}", 1, 1, 1, f"Section{random.randint(1, 2)}")