from abc import ABC, abstractmethod

from model.Ativos import Ativo


class Repo(ABC):
    @abstractmethod
    def insert(self, ativo: Ativo) -> None: pass
    @abstractmethod
    def find_all(self): pass
    @abstractmethod
    def find_by_id(self, id): pass
    @abstractmethod
    def find_by_nome(self, nome): pass
    @abstractmethod
    def update(self, ativo: Ativo) -> None: pass
    @abstractmethod
    def delete_ativo(self, id)-> None: pass