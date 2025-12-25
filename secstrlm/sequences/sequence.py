import copy
from collections import Counter
from typing import Iterator, List, Dict, Optional, Union, Tuple
from .features import Features
from ..types.molecules import MoleculeTypes
from secstrlm.sequences.features import Features


class Sequence:
    
    def __init__(self, sequence: str, 
                 name: str = 'Teo1') ->None:
        self.__sequence = sequence.upper()
        self.__name = name
        self.__features = Features()

    @property
    def sequence(self) -> str:
        return self.__sequence
    
    @sequence.setter
    def sequence(self, sequence: str) -> None:
        self.__sequence = sequence.upper()
        
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str) -> None:
        self.__name = name
        
    @property
    def features(self) -> Features:
        return self.__features

    @features.setter
    def features(self, features: Features) -> None:
        self.__features = features
    
    def __len__(self) -> int:
        return len(self.__sequence)
    
    def __contains__(self, item: str) -> bool:
        return item.upper() in self.__sequence
    
    def __eq__(self, value:"Sequence") -> bool:
        return self.__sequence == value.sequence
    
    def __iter__(self) -> Iterator[str]:
        return iter(self.__sequence)
    
    def __getitem__(self, key: slice) -> 'Sequence':
        f = copy.deepcopy(self.__features)
        f.add('start', key.start)
        return self.__class__(self.__sequence[key], name=self.__name, features=f)
    
    def __repr__(self):
        seq = self.__sequence if len(self) < 80 else self.__sequence[:40] + "..." + self.__sequence[-40:]
        name = self.name if self.name else "Unknown"
        return f"{name}: {seq} [{len(self)}]"
        
    def sliding(self, size: int) -> Iterator[tuple[int, 'Sequence']]:
        for i in range(len(self) - size + 1):
            yield i, self[i:i+size]
            
class Dna(Sequence):
    
    def __init__(self,
                 sequence: Union[str, Sequence],
                 name: str = "Unknown",
                 direction: Tuple[int, int] = (5, 3)) -> None:
        if isinstance(sequence, Sequence):
            super().__init__(sequence.sequence, sequence.name)
            super().features = sequence.features
        else:
            super().__init__(sequence, name)
        self.__direction: Tuple[int, int] = direction
        self.__type = MoleculeTypes.DNA
        
    @property
    def type(self) -> MoleculeTypes:
        return self.__type
    
    def complement(self) -> 'Dna':
        complement_map = str.maketrans('ATCG', 'TAGC')
        comp_sequence = self.sequence.translate(complement_map)
        temp = Dna(comp_sequence, name=self.name + "_comp", direction=(self.__direction[1], self.__direction[0]))
        temp.features = self.features
        return temp
    
    def reverse(self) -> 'Dna':
        rev_sequence = self.sequence[::-1]
        temp = Dna(rev_sequence, name=self.name + "_rev", direction=(self.__direction[1], self.__direction[0]))
        temp.features = self.features
        return temp
    
    def __repr__(self) -> str:
        seq = self.sequence if len(self) < 80 else self.sequence[:40] + "..." + self.sequence[-40:]
        name = self.name if self.name else "Unknown"
        return f"{name}:{self.__direction[0]}'-{seq}-{self.__direction[1]}' [{len(self)}] <{self.__type.value}>"
          
class Rna(Sequence):
    
    def __init__(self,
                 sequence: Union[str, Sequence],
                 name: str = "Unknown",
                 direction: Tuple[int, int] = (5, 3)) -> None:
        if isinstance(sequence, Sequence):
            super().__init__(sequence.sequence.replace('T', 'U'),
                             sequence.name)
            super().features = sequence.features
        else:
            super().__init__(sequence.replace('T', 'U'), name)
        self.__direction: Tuple[int, int] = direction
        self.__type = MoleculeTypes.RNA
        
    @property
    def type(self) -> MoleculeTypes:
        return self.__type
    
    def complement(self) -> 'Rna':
        complement_map = str.maketrans('AUCG', 'UAGC')
        comp_sequence = self.sequence.translate(complement_map)
        temp = Rna(comp_sequence, name=self.name + "_comp", direction=(self.__direction[1], self.__direction[0]))
        temp.features = self.features
        return temp
    
    def reverse(self) -> 'Rna':
        rev_sequence = self.sequence[::-1]
        temp = Rna(rev_sequence, name=self.name + "_rev", direction=(self.__direction[1], self.__direction[0]))
        temp.features = self.features
        return temp
    
    def __repr__(self) -> str:
        seq = self.sequence if len(self) < 80 else self.sequence[:40] + "..." + self.sequence[-40:]
        name = self.name if self.name else "Unknown"
        return f"{name}:{self.__direction[0]}'-{seq}-{self.__direction[1]}' [{len(self)}] <{self.__type.value}>"

class Protein(Sequence):

    def __init__(self,
                 sequence: Union[str, Sequence],
                 name: str = "Unknown") -> None:
        if isinstance(sequence, Sequence):
            super().__init__(sequence.sequence, sequence.name)
            super().features = sequence.features
        else:
            super().__init__(sequence, name)
        self.__type = MoleculeTypes.PROTEIN
        
    @property
    def type(self) -> MoleculeTypes:
        return self.__type
     
    def __repr__(self) -> str:
        seq = self.sequence if len(self) < 80 else self.sequence[:40] + "..." + self.sequence[-40:]
        name = self.name if self.name else "Unknown"
        return f"{name}:-{seq}-[{len(self)}] <{self.__type.value}>"
