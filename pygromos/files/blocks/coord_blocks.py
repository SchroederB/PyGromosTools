from enum import Enum
from typing import List, Iterable
from numbers import Number

from pygromos.files.blocks._general_blocks import _generic_gromos_block, _generic_field, _iterable_gromos_block
from pygromos.files.blocks._general_blocks import TITLE, TIMESTEP, TRAJ

# forward declarations
TITLE:TITLE = TITLE
TIMESTEP:TIMESTEP = TIMESTEP
TRAJ:TRAJ = TRAJ


##########################################################################
#   ENUMS
##########################################################################

class Pbc(Enum):
    trunc_octahedron = -1
    vacuum = 0
    rectangular = 1
    triclinic = 2

##########################################################################
#   FIELDS
##########################################################################

class atomP(_generic_field):
    def __init__(self, resID:int, resName:str, atomType:str, atomID:int, xp:float, yp:float, zp:float):
        """

        Parameters
        ----------
        resID
        resName
        atomType
        atomID
        xp
        yp
        zp
        """
        self.resID = resID
        self.resName = resName
        self.atomType = atomType
        self.atomID = atomID
        self.xp = xp
        self.yp = yp
        self.zp = zp

    def to_string(self) -> str:
        return "{: >5} {: <5} {: <6} {: >5}{: 15.9f}{:15.9f}{:15.9f}\n".format(self.resID, self.resName, self.atomType, self.atomID, self.xp,
                                                                               self.yp, self.zp)


class atomV(_generic_field):
    def __init__(self, resID:int, resName:str, atomType:str, atomID:int, xv:float, yv:float, zv:float):
        self.resID = resID
        self.resName = resName
        self.atomType = atomType
        self.atomID = atomID
        self.xv = xv
        self.yv = yv
        self.zv = zv

    def to_string(self) -> str:
        return "{: >5} {: >3}  {: <5}{: >7}{: 15.9f}{:15.9f}{:15.9f}\n".format(self.resID, self.resName, self.atomType, self.atomID, self.xv,
                                                                               self.yv, self.zv)


class lattice_shift(_generic_field):
    def __init__(self, atomID:int, x:float, y:float, z:float):
        self.atomID = atomID
        self.x = x
        self.y = y
        self.z = z

    def to_string(self) -> str:
        return "{:>10}{:>10}{:>10}\n".format(self.x, self.y, self.z)

class atomSI(_generic_field):
    def __init__(self, resID: int, resName: str, atomType: str, atomID: int, sxx: float, sxy: float, sxz: float):
        self.resID = resID
        self.resName = resName
        self.atomType = atomType
        self.atomID = atomID
        self.sxx = sxx
        self.sxy = sxy
        self.sxz = sxz

    def to_string(self) -> str:
        return "{: >5} {: >3}  {: <5}{: >7}{: 15.9f}{:15.9f}{:15.9f}\n".format(self.resID, self.resName, self.atomType, self.atomID, self.sxx,
                                                                               self.sxy, self.sxz)

##########################################################################
#   BLOCKS
##########################################################################


class POSITION(_iterable_gromos_block):
    """
        POSITION

        Parameters
        ----------
        content: List[atomP]
            every element in this list is of atom position obj

    """
    def __init__(self, content: List[atomP]):
        super().__init__(used=True, name="POSITION")
        self.content = content

class POSRESSPEC(_iterable_gromos_block):
    """
        POSITION

        Parameters
        ----------
        content: List[atomP]
            every element in this list is of atom position obj

    """
    def __init__(self, content: List[atomP]):
        super().__init__(used=True, name="POSRESSPEC")
        self.content = content

class VELOCITY(_iterable_gromos_block):
    """
        VELOCITY

        Parameters
        ----------
        content: List[atomV]
            every element in this list is of atom velocity obj

    """

    def __init__(self, content: List[atomV]):
        super().__init__(used=True, name="VELOCITY")
        self.content = content

class STOCHINT(_iterable_gromos_block):
    """
        STOCHINT

        Parameters
        ----------
        content: List[atomSI]
            every element in this list is of atom stochastic interval obj

        seed: str
            contains the seed for the stochastic dynamics simulation
    """

    def __init__(self, content: List[atomSI], seed: str):
        super().__init__(used=True, name="STOCHINT")
        self.content = content
        self.seed = seed
        #print(self.seed)

    def to_string(self) -> str:
        return self.content + self.seed


class REFPOSITION(_iterable_gromos_block):
    """
        REFPOSITION

        Parameters
        ----------
        content: List[atomP]
            every element in this list is of atom position obj

    """

    def __init__(self, content: List[atomP]):
        """

        Parameters
        ----------
        content: List[atomP]
            every element in this list is of atom position obj

        """
        super().__init__(used=True, name="REFPOSITION")
        self.content = content


class LATTICESHIFTS(_iterable_gromos_block):
    """
        LATTICESHIFTS

        Parameters
        ----------
        content: List[lattice_shift]
            every element in this list is a lattice shift obj

    """

    def __init__(self, content: List[lattice_shift]):
        """

        Parameters
        ----------
        content: List[lattice_shift]
            every element in this list is a lattice shift obj
        """
        super().__init__(used=True, name="LATTICESHIFTS")
        self.content = content


class GENBOX(_generic_gromos_block):
    '''GENBOX

        This Block is representing the simulation Box in a coordinate file.

    Attributes
    ----------
    pbc: int,Pbc
        Periodic Boundary Condition
    length: List[float]
    angles: List[float]
    euler: List[float]
    origin: List[float]

    '''

    def __init__(self, pbc: Pbc=Pbc(0), length: List[float] = [0.0,0.0,0.0], angles: List[float] = [0.0,0.0,0.0], euler: List[float] = [0.0,0.0,0.0], origin: List[float] = [0.0,0.0,0.0]):
        '''

        Parameters
        ----------
        pbc: int,Pbc
        length: List[float]
        angles: List[float]
        euler: List[float]
        origin: List[float]

        '''

        super().__init__(used=True, name="GENBOX")
        self._pbc = Pbc(pbc)
        self._length = length
        self._angles = angles
        self._euler = euler
        self._origin = origin

    def block_to_string(self) -> str:
        result = self.name + "\n"
        result += "{:>5}\n".format(str(self.pbc.value))
        result += "{:>15.9f}{:>15.9f}{:>15.9f}\n".format(self.length[0], self.length[1], self.length[2])
        result += "{:>15.9f}{:>15.9f}{:>15.9f}\n".format(self.angles[0], self.angles[1], self.angles[2])
        result += "{:>15.9f}{:>15.9f}{:>15.9f}\n".format(self.euler[0], self.euler[1], self.euler[2])
        result += "{:>15.9f}{:>15.9f}{:>15.9f}\n".format(self.origin[0], self.origin[1], self.origin[2])
        result += "END\n"

        return result

    #Attributes
    @property
    def pbc(self)->Pbc:
        return self._pbc
    @pbc.setter
    def pbc(self, pbc: Pbc):
        if(isinstance(pbc, Pbc)):
            self._pbc = pbc
        elif(isinstance(pbc, int) or (isinstance(pbc, str) and pbc.isalnum())):
            if(int(pbc) in Pbc._value2member_map_):
                self._pbc = Pbc(int(pbc))
            else:
                raise ValueError("unknown int for pbc\n Use: \n"+str(Pbc.__members__))
        else:
            raise ValueError("Periodic boundary Condition must be int or PBC-Enum")
    @property
    def length(self) -> List[float]:
        return self._length
    @length.setter
    def length(self, length: List[float]):
        if(isinstance(length, List) and all([isinstance(x, Number) for x in length])):
            self._length = length
        else:
            raise ValueError("length must be List[float]")
    @property
    def angles(self) -> List[float]:
        return self._angles
    @angles.setter
    def angles(self, angles: List[float]):
        if(isinstance(angles, List) and all([isinstance(x, Number) for x in angles])):
            self._angles = angles
        else:
            raise ValueError("angles must be List[float]")
    @property
    def euler(self) -> List[float]:
        return self._euler
    @euler.setter
    def euler(self, euler: List[float]):
        if(isinstance(euler, List) and all([isinstance(x, Number) for x in euler])):
            self.euler = euler
        else:
            raise ValueError("euler must be List[float]")
    @property
    def origin(self) -> List[float]:
        return self._origin
    @origin.setter
    def origin(self, origin: List[float]):
        if(isinstance(origin, List) and all([isinstance(x, Number) for x in origin])):
            self._angles = origin
        else:
            raise ValueError("origin must be List[float]")


class PERTDATA(_generic_gromos_block):

    content: float
    def __init__(self, lam: float):
        """
           This block is used for lambda-sampling and gives the lambda value of the current coordinates.

        Parameters
        ----------
        lambda_value: float
            current lambda value
        """
        super(PERTDATA, self).__init__(name=__class__.__name__, used=True)
        self.content = float(lam)
        
    @property
    def lam(self)->float:
        return self.content

    @lam.setter
    def lam(self, lam:float):
        self.content = float(lam)