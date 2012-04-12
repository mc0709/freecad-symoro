from joint import Joint
from chain import Chain
from chain import get_children

dummy_jnt_parameters = {
    'mu': 0,
    'sigma': 0,
    'gamma': 0,
    'b': 0,
    'alpha':0,
    'd':0,
    'theta': 0,
    'r': 0,
    }

jnt1 = Joint(antc=None, **dummy_jnt_parameters)
jnt2 = Joint(antc=jnt1, **dummy_jnt_parameters)
jnt3 = Joint(antc=jnt2, **dummy_jnt_parameters)
jnt4 = Joint(antc=jnt2, **dummy_jnt_parameters)
jnt5 = Joint(antc=jnt4, **dummy_jnt_parameters)
joints = [jnt1, jnt2, jnt3]
#print(jnt1)
#print(jnt2)
#print(jnt3)
#print(jnt4)
#print(jnt5)

chain = Chain(joints)
#print([chain.get_subchain(jnt) for jnt in get_children(joints, jnt1)])
assert(chain.bases == [jnt1])
assert(chain.tools == [jnt3])
assert(get_children(joints, jnt1) == [jnt2])
assert(get_children(joints, jnt2) == [jnt3])
assert(chain.get_subchain(jnt3) == [jnt3])
assert(chain.get_subchain(jnt2) == [jnt2, jnt3])
assert(chain.get_subchain(jnt1) == [jnt1, jnt2, jnt3])

joints = [jnt1, jnt2, jnt3, jnt4]
chain = Chain(joints)
assert(chain.bases == [jnt1])
assert(chain.tools == [jnt3, jnt4])
assert(get_children(joints, jnt1) == [jnt2])
assert(get_children(joints, jnt2) == [jnt3, jnt4])
assert(chain.get_subchain(jnt3) == [jnt3])
assert(chain.get_subchain(jnt4) == [jnt4])
assert(chain.get_subchain(jnt2) == [jnt2, [[jnt3], [jnt4]]])
assert(chain.get_subchain(jnt1) == [jnt1, jnt2, [[jnt3], [jnt4]]])

chain = Chain([jnt1, jnt2, jnt3, jnt4, jnt5])
assert(chain.tools == [jnt3, jnt5])
assert(chain.get_subchain(jnt4) == [jnt4, jnt5])
assert(chain.get_subchain(jnt1) == [jnt1, jnt2, [[jnt3], [jnt4, jnt5]]])

