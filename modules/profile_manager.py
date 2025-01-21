import json
import os
from colorama import Fore

class ProfileManager:
    def __init__(self):
        self.profiles_file = "profiles.json"
        self.profiles = self._load_profiles()

    def _load_profiles(self):
        """Carrega os perfis do arquivo JSON"""
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_profiles(self):
        """Salva os perfis no arquivo JSON"""
        with open(self.profiles_file, 'w') as f:
            json.dump(self.profiles, f, indent=4)

    def add_profile(self, name, keys):
        """Adiciona ou atualiza um perfil"""
        self.profiles[name] = keys
        self._save_profiles()

    def remove_profile(self, name):
        """Remove um perfil"""
        if name in self.profiles:
            del self.profiles[name]
            self._save_profiles()
            return True
        return False

    def get_profile(self, name):
        """Retorna as chaves de um perfil específico"""
        return self.profiles.get(name, [])

    def list_profiles(self):
        """Retorna lista de nomes dos perfis"""
        return list(self.profiles.keys())

    def profile_exists(self, name):
        """Verifica se um perfil existe"""
        return name in self.profiles 