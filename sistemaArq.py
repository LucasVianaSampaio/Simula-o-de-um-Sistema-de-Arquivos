
class INode:
    def __init__(self, name, is_dir=False):
        self.name = name
        self.size = 0
        self.blocks = []
        self.is_dir = is_dir
        self.children = {} if is_dir else None
        self.parent = None

    def add_block(self, data):
        self.blocks.append(data)
        self.size += len(data)

    def read_blocks(self):
        return ''.join(self.blocks) if self.blocks else "(vazio)"
    
class FileSystem:
    def __init__(self):
        self.root = INode("/", is_dir=True)
        self.current_dir = self.root

    def create(self, name, is_dir=False):
        if name in self.current_dir.children:
            print(f"Erro: '{name}' já existe")
            return
        new_node = INode(name, is_dir=is_dir)
        new_node.parent = self.current_dir
        self.current_dir.children[name] = new_node
        print(f"{'Diretório' if is_dir else 'Arquivo'} '{name}' criado com sucesso.")

    def list_dir(self):
        print(f"Conteúdo de {self.current_dir.name}:")
        for item in self.current_dir.children.values():
            tipo = "DIR" if item.is_dir else "ARQ"
            print(f"{tipo}: {item.name} (tamanho: {item.size} bytes)")

    def navigate(self, dir_name):
        if dir_name == "..":
            if self.current_dir.parent:
                self.current_dir = self.current_dir.parent
            else:
                print("Você já está na raiz")
        elif dir_name == ".":
            pass
        elif dir_name in self.current_dir.children and self.current_dir.children[dir_name].is_dir:
            self.current_dir = self.current_dir.children[dir_name]
        else:
            print(f"Erro: '{dir_name}' não é um diretório")
        print(f"Diretório atual: {self.current_dir.name}")
    
    def move(self, file_name, target_dir_name):
        if file_name not in self.current_dir.children:
            print(f"Erro: '{file_name}' não existe no diretório atual")
            return
        if target_dir_name not in self.current_dir.children or not self.current_dir.children[target_dir_name].is_dir:
            print(f"Erro: '{target_dir_name}' não é um diretório")
            return

        node = self.current_dir.children.pop(file_name)
        target_dir = self.current_dir.children[target_dir_name]
        node.parent = target_dir
        target_dir.children[file_name] = node
        print(f"Arquivo '{file_name}' movido para '{target_dir_name}' com sucesso")

    def write_file(self, file_name, data):
        if file_name not in self.current_dir.children or self.current_dir.children[file_name].is_dir:
            print(f"Erro: '{file_name}' não é um arquivo")
            return
        inode = self.current_dir.children[file_name]
        inode.add_block(data)
        print(f"Dados escritos no arquivo '{file_name}'")

    def read_file(self, file_name):
        if file_name not in self.current_dir.children or self.current_dir.children[file_name].is_dir:
            print(f"Erro: '{file_name}' não é um arquivo")
            return
        inode = self.current_dir.children[file_name]
        print(f"Conteúdo de '{file_name}': {inode.read_blocks()}")
    
    def delete(self, name):
        if name not in self.current_dir.children:
            print(f"Erro: '{name}' não existe no diretório atual")
            return
        inode = self.current_dir.children[name]
        if inode.is_dir and inode.children:
            print(f"Erro: o diretório '{name}' não está vazio")
            return
        self.current_dir.children.pop(name)
        print(f"{'Diretório' if inode.is_dir else 'Arquivo'} '{name}' excluído com sucesso")

def main():
    fs = FileSystem()

    while True:
        comando = input("\nComando (criar, ls, cd, mover, ler, escrever, excluir, sair): ").strip().lower()

        if comando == "sair":
            break
        elif comando.startswith("criar"):
            _, nome, tipo = comando.split()
            fs.create(nome, is_dir=(tipo == "dir"))
        elif comando == "ls":
            fs.list_dir()
        elif comando.startswith("cd"):
            _, dir_name = comando.split()
            fs.navigate(dir_name)
        elif comando.startswith("mover"):
            _, file_name, target_dir_name = comando.split()
            fs.move(file_name, target_dir_name)
        elif comando.startswith("escrever"):
            _, nome_arquivo, dados = comando.split(maxsplit=2)
            fs.write_file(nome_arquivo, dados)
        elif comando.startswith("ler"):
            _, nome_arquivo = comando.split()
            fs.read_file(nome_arquivo)
        elif comando.startswith("excluir"):
            _, nome = comando.split()
            fs.delete(nome)
        else:
            print("Comando não reconhecido")

if __name__ == "__main__":
    main()
