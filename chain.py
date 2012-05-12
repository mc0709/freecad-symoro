#!/usr/bin/python
# -*- encoding: utf-8 -*-

def get_base(joints):
    """Return the base joint, i.e. joints without antecedant"""
    base = None
    for jnt in joints:
        if not(jnt.antc in joints):
            base = jnt
    return base

def get_tools(joints):
    """Return the end joints, i.e. joints that are antecedant of nothing"""
    antc = [jnt.antc for jnt in joints]
    # A joint is an end joint if is antecedant of no other joints.
    tools = [jnt for jnt in joints if not(jnt in antc)]
    return tools

def get_children(joints, joint):
    """Return a list of joints which have the given joint as antecedant"""
    return [jnt for jnt in joints if (jnt.antc is joint)]

def is_unique_child(joint, joints):
    """Return True is no other joint has the same antecedant"""
    antc = [jnt.antc for jnt in joints]
    return (antc.count(joint.antc) == 1)

def get_subchain_to(joint, joints):
    """Return the subchain ending at joint"""
    if not(joint.antc in joints):
        return [joint]
    l = []
    l.extend(get_subchain_to(joint=joint.antc, joints=joints))
    l.append(joint)
    return l

class Chain(object):
    def __init__(self, joints):
        self.joints = joints
        self._base = get_base(joints)
        if self._base is None:
            raise ValueError('Chain has no base joint')
        self._tools = get_tools(joints)

    @property
    def base(self):
        """The base joint, i.e. joints without antecedant"""
        return self._base

    @property
    def tools(self):
        """The end joints, i.e. joints that are antecedant of nothing"""
        return self._tools

    def get_subchain_from(self, joint):
        """Return the subchain starting at joint"""
        subjnts = get_children(self.joints, joint)
        if (len(subjnts) == 0):
            return [joint]
        elif (len(subjnts) == 1):
            return [joint] + self.get_subchain_from(subjnts[0])
        else:
            l = [joint]
            l.append([self.get_subchain_from(jnt) for jnt in subjnts])
            return l

    def get_subchain_to(self, joint):
        """Return the subchain ending at joint"""
        return get_subchain_to(joint=joint, joints=self.joints)

    def get_chain(self):
        return self.get_subchain_from(self.base)

    def get_mjoints(self):
        """Return a list of non-fixed joints"""
        mjoints = []
        for jnt in self.joints:
            if jnt.ismoving():
                mjoints.append(jnt)
        return mjoints



