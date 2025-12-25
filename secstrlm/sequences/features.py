from typing import Iterator

class Qalifier:
    
    def __init__(self, qualifier:str, value:str) -> None:
        self.__qualifier = qualifier
        self.__value = value
    
    @property
    def qualifier(self) -> str:
        return self.__qualifier
    
    @qualifier.setter
    def qualifier(self, qualifier:str) -> None:
        self.__qualifier = qualifier
        
    @property
    def value(self) -> str:
        return self.__value
    
    @value.setter
    def value(self, value:str) -> None:
        self.__value = value

    def __repr__(self):
        return f"{self.__qualifier}:{self.__value}"
    
    def __eq__(self, other):
        if not isinstance(other, Qalifier):
            return False
        return self.__qualifier == other.qualifier and self.__value == other.value
    
    def __hash__(self):
        return hash((self.__qualifier, self.__value))

class Feature:
    
    def __init__(self, feature_type:str, location:str) -> None:
        self.__feature_type = feature_type
        self.__location = location
        self.__qualifiers = []
    
    @property
    def feature_type(self) -> str:
        return self.__feature_type
    
    @property
    def location(self) -> str:
        return self.__location
    
    def add(self, qualifier:str, value:str) -> None:
        self.__qualifiers.append(Qalifier(qualifier, value))
    
    def list(self) -> list:
        return [q.qualifier for q in self.__qualifiers]
    
    def get(self, qualifier:str) -> list:
        return [q.value for q in self.__qualifiers if q.qualifier == qualifier]
    
    def remove(self, qualifier:str, value:str) -> bool:
        temp = Qalifier(qualifier, value)
        if temp in self.__qualifiers:
            self.__qualifiers.remove(temp)
            return True
        raise ValueError(f"{temp} not found.")
        
    def __len__(self) -> int:
        return len(self.__qualifiers)
    
    def __iter__(self) -> Iterator[Qalifier]:
        return iter(self.__qualifiers)
    
    def __getitem(self, slice) -> Qalifier:
        return self.__qualifiers[slice]
    
class Features:
    
    def __init__(self) -> None:
        self.__features = []
    
    def add(self, feature_type:str, location:str) -> Feature:     
        feature = Feature(feature_type, location)
        self.__features.append(feature)
        return feature
    
    def list(self) -> list:
        return [f.feature_type for f in self.__features]
    
    def get(self, feature_type:str) -> list:
        return [f for f in self.__features if f.feature_type == feature_type]
    
    def remove(self, feature_type:str, location:str) -> bool:
        temp = Feature(feature_type, location)
        for f in self.__features:
            if f.feature_type == temp.feature_type and f.location == temp.location:
                self.__features.remove(f)
                return True
        raise ValueError(f"{temp} not found.")
    
    def __len__(self) -> int:
        return len(self.__features) 
    
    def __iter__(self) -> Iterator[Feature]:
        return iter(self.__features)
    
    def __getitem__(self, slice) -> Feature:
        return self.__features[slice]
    
    
    