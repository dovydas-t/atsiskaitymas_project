import pickle

class FileHandler:
    @staticmethod
    def read_from_pickle(file_path, default_value):
        try:
            with open(file_path, "rb") as file:
                data = pickle.load(file)
                return data
        except (FileNotFoundError, EOFError):
            return default_value

    @staticmethod
    def write_to_pickle(file_path, data):
        try:
            with open(file_path, "wb") as file:
                pickle.dump(data, file)
                return True
        except Exception as e:
            return False