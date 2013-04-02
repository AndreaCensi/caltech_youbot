import numpy as np    

# Constructors

def constraint_none(desc):
    return {'constraint-type': 'none', 'desc': desc}

def constraint_plane(plane, desc):
    return {'constraint-type': 'plane', 'desc': desc, 'plane': plane}

# Integrity check

def assert_valid_constraint(c):
    assert isinstance(c, dict)
    assert 'constraint-type' in c
    assert c['constraint-type'] in ['none', 'plane']

# Respecting constraints

def constraint_respected_by_twist(c, twist):
    """ Retunrs bool, string """
    assert_valid_constraint(c)
    if c['constraint-type'] == 'none':
        return True, c['desc']
    elif c['constraint-type'] == 'plane':
        plane = np.array(c['plane'])
        x = np.array([twist.linear.x, twist.linear.y])
        val = np.sum(plane * x)
        if val < 0:
            msg = ' %s * %s = %s < 0' % (plane, x, val)
            return False, msg
        else:
            return True, ''
    else:
        assert False
    
def constraints_respected_by_twist(constraints, twist):
    whys = []
    result = True
    for c in constraints:
        respected, why = constraint_respected_by_twist(c, twist)
        if not respected:
            result = False
            whys.append(why)
    reason = ";".join(whys)
    return result, reason
