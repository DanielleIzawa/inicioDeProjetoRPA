import os
import subprocess
import argparse
from pathlib import Path
import platform

# Define o conteúdo de cada arquivo
# O .gitignore foi modificado para refletir as suas exclusões e as pastas do venv criado na raiz.
CUSTOM_GITIGNORE_CONTENT = """Include/
Lib/
Scripts/
bin/

*.cfg
*/__pycache__/
.vscode/
"""

FILE_CONTENTS = {
    "main.py": """from src.robo import start

start()
""",
    "src/robo.py": """from src.robo_params import *

def start():
    print('Projeto iniciado')
    return True
""",
    "src/robo_params.py": "# Adicione aqui os parâmetros da sua automação\n",
    ".gitignore": CUSTOM_GITIGNORE_CONTENT, # Conteúdo inicial
    "requirements.txt": "# Adicione as dependências do projeto aqui\n",
    "README.md": "# {project_name}\n\nEste é o projeto de automação {project_name}.\n"
}

def create_project_structure(project_path, project_name):
    """Cria a estrutura de diretórios e arquivos para o projeto."""
    print(f"Iniciando a criação do projeto '{project_name}'...")

    # Garante que o diretório raiz do projeto exista
    project_path.mkdir(exist_ok=True)

    # Cria as subpastas
    (project_path / "src").mkdir(exist_ok=True)
    (project_path / "components").mkdir(exist_ok=True)

    # Cria os arquivos com seu respectivo conteúdo
    for file_path_str, content in FILE_CONTENTS.items():
        # **Atenção:** NÃO criamos o .gitignore aqui, pois ele será sobrescrito pelo venv.
        # Vamos criá-lo APÓS a criação do venv para garantir o seu conteúdo.
        if file_path_str == ".gitignore":
            continue
            
        file_path = project_path / file_path_str

        # Substitui o placeholder pelo nome do projeto no README
        if file_path_str == "README.md":
            content = content.format(project_name=project_name)

        file_path.write_text(content, encoding='utf-8')
        print(f"  -> Arquivo criado: {file_path}")

    print("\nEstrutura de arquivos e pastas criada com sucesso.")
    project_name = project_path.name
    
    structure_output = f"""
======================================================================
✅ Projeto {project_name} inicializado com sucesso!
======================================================================
A estrutura padrão do projeto segue a seguinte organização:
{project_name}/
├── components/         # Componentes para interação com sistemas externos
├── src/
│   ├── robo.py         # Lógica da automação
│   └── robo_params.py  # Dados de parametrização
├── main.py             # Ponto de entrada do robô
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação do projeto
======================================================================
"""
        
    print(structure_output) 
    return project_path

def setup_virtual_environment(project_path: Path, custom_gitignore_content: str):
    """
    Cria o ambiente virtual DENTRO da pasta do projeto e exibe o comando de ativação.
    Em seguida, sobrescreve o .gitignore para garantir o conteúdo desejado.
    """
    print("\nConfigurando o ambiente virtual (venv)...")
    
    # 1. Cria o ambiente virtual
    try:
        subprocess.run(["python", "-m", "venv", "."], check=True, cwd=project_path)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar o ambiente virtual: {e}")
        print("Certifique-se de que o Python esteja instalado e no PATH.")
        return
        
    print("Ambiente virtual criado na pasta raiz do projeto.")

    # 2. SOBRESCREVE o .gitignore com o conteúdo desejado
    gitignore_path = project_path / ".gitignore"
    try:
        gitignore_path.write_text(custom_gitignore_content, encoding='utf-8')
        print(f"  -> Arquivo criado/atualizado: {gitignore_path} (com o conteúdo desejado)")
    except Exception as e:
        print(f"❌ Aviso: Não foi possível sobrescrever o .gitignore. Erro: {e}")
        
    # 3. Exibe a mensagem de ativação
    system = platform.system()
    
    if system == "Windows":
        activation_command_cmd = f"source .\\Scripts\\activate"
        activation_command_bash = f"source Scripts/activate"
        
        print("\n" + "="*70)
        print("\nPara ativar o ambiente virtual e execute:")
        print("\n 💻 Para Prompt de Comando (CMD/PowerShell) do Windows:")
        print(f"   {activation_command_cmd}")
        print("\n 🐧 Para ambientes BASH (Git Bash/WSL):")
        print(f"   {activation_command_bash}")
        print("\n" + "="*70)
        
    else: # Linux ou macOS
        activation_command = f"source bin/activate"

        print("\n" + "="*70)
        print("✅ Projeto inicializado com sucesso!")
        print(f"\nPara ativar o ambiente virtual e execute:")
        print(f"\n   {activation_command}\n")
        print("="*70)

def main():
    """Função principal para executar a CLI."""
    parser = argparse.ArgumentParser(
        description="CLI para inicializar um novo projeto de automação com uma estrutura pré-definida."
    )
    parser.add_argument(
        "project_name",
        type=str,
        nargs='?', # Torna o argumento posicional opcional
        default=None,
        help="O nome do projeto a ser criado. Se não for fornecido, a estrutura será criada no diretório atual."
    )
    
    args = parser.parse_args()
    
    if args.project_name:
        project_path = Path(args.project_name)
        project_name_for_content = args.project_name
    else:
        project_path = Path.cwd()
        project_name_for_content = project_path.name

    try:
        # 1. Cria a estrutura (sem o .gitignore por enquanto)
        create_project_structure(project_path, project_name_for_content)
        
        # 2. Configura o ambiente virtual e, em seguida, sobrescreve o .gitignore
        setup_virtual_environment(project_path, CUSTOM_GITIGNORE_CONTENT) 
        
    except Exception as e:
        print(f"\n❌ Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()