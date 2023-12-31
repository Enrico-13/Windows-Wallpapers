import os
import shutil
from PIL import Image
from tqdm import tqdm
from time import sleep

# pega o nome do usuário
user = os.path.expanduser("~")
# define o caminho dos wallpapers
dir = os.path.join(user, 'AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets')
# pega a pasta atual
curdir = os.getcwd()

# checa se as pastas mobile e desktop existem, e cria se for necessário
curdir_desktop = os.path.join(curdir, 'desktop')
curdir_mobile = os.path.join(curdir, 'mobile')
if not os.path.exists(curdir_desktop):
    os.mkdir(curdir_desktop)
if not os.path.exists(curdir_mobile):
    os.mkdir(curdir_mobile)

count_desktop = 0
count_mobile = 0

# pega cada arquivo dentro da pasta dos wallpapers
for file in tqdm(os.listdir(dir), desc='Gerando Wallpapers: ', colour='#4169E1'):
    sleep(0.1)
    new_filepath = None
    try:
        # cria um caminho incluindo o arquivo atual
        old_filepath = os.path.join(dir, file)
        # cria o nome novo do arquivo, com a extensão jpg
        new_name = file + '.jpg'
        # copia o arquivo da pasta dos wallpapers para a pasta atual
        shutil.copy2(old_filepath, curdir)
        
        # cria um nome temporário para o arquivo sem a extensão jpg
        temp_filepath = os.path.join(curdir, file)
        # cria um nome temporário para o arquivo com a extensão jpg
        temp_filepath_name = os.path.join(curdir, new_name)

        # renomea o arquivo e adiciona a extensão jpg
        os.rename(temp_filepath, temp_filepath_name)

        # abre a imagem numa variável temporária "img"
        with Image.open(temp_filepath_name) as img:
            # se a altura da imagem for menor que o comprimento, cria o caminho para a pasta desktop
            if img.height < img.width:
                new_filepath = curdir_desktop
            # se a altura da imagem for menor que o comprimento, cria o caminho para a pasta mobile
            elif img.height > img.width:
                new_filepath = curdir_mobile

        # se a variável new_filepath não existir, caso a altura e o comprimento sejam os mesmos, deleta o arquivo temporário
        if not new_filepath:
            os.remove(temp_filepath_name)

        # move o arquivo para a pasta destino
        else:
            shutil.move(temp_filepath_name, new_filepath)
            if new_filepath == curdir_desktop:
                count_desktop += 1
            else:
                count_mobile += 1

    except FileExistsError:
        os.remove(temp_filepath_name)

    except shutil.Error:
        os.remove(temp_filepath_name)

    except FileNotFoundError:
        pass


print(f"{count_desktop} wallpapers desktop e {count_mobile} wallpapers mobile foram criados.")
input("Aperte ENTER para finalizar.")
