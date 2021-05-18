import os
import pathlib
import shutil
import string
import sys

cortFolder = ("folder")
cortImage = ("jpeg", "png", "jpg", "svg")
cortVideo = ("avi", "mp4", "mov", "mpg")
cortText = ("doc", "dcox", "txt", "odt")
cortMusic = ("mp3", "ogg", "wav", "amr")
cortArchive = ("zip", "eg", "tar", "gz")
cortVarious = ("max", "vsd", "blend", "")

def inputing(path):
    try:
        listContain = os.listdir(path)
    except NotADirectoryError:
        listContain = inputing(path = input("\nReenter your directory, please "))
    except FileNotFoundError:
        listContain = inputing(path = input("\nReenter your directory, please "))
    oldpath = path
    return listContain, oldpath

def outputing(dictFiles):
    os.system("clear")
    find = input("Enter that you wanna find (folder, image, video, text, musics, archive, various or all) or exit\t")
    key = list(dictFiles.keys())
    if find == "folder":
        i = 0
        print(f"\nList of folders ({key[i]})\n")
    elif find == "image":
        i = 1
        print(f"\nList of images ({key[i]})\n")
    elif find == "video":
        i = 2
        print(f"\nList of video files ({key[i]})\n")
    elif find == "text":
        i = 3
        print(f"\nList of documents ({key[i]})\n")
    elif find == "music":
        i = 4
        print(f"\nList of music files ({key[i]})\n")
    elif find == "archive":
        i = 5
        print(f"\nList of archive files ({key[i]})\n")
    elif find == "various":
        i = 6
        print(f"\nList of various files ({key[i]})\n")
    elif find == "all":
        for key, value in dictFiles.items():
            print(f"\nList of contains ({key}) : {value}\n")
    elif find == "exit":
        input("\nPress any key to outside")
        return None
    if find != "all":
        try:
            for value in dictFiles.get(key[i]):
                print(f"{value}\n")
        except NameError:
            print("\nYou maked the fail by inputing the command for search")
    input("\nPress any key to continue")
    outputing(dictFiles)

def sorting(contains, oldpath):

    dictFiles = {cortFolder: [], cortImage: [], cortVideo: [], cortText: [], cortMusic: [], cortArchive: [], cortVarious: []}
    os.chdir(oldpath)
    for contain in contains:
        if pathlib.Path(contain).is_file():
            j = 0
            while not (contain.endswith(cortImage[j]) or contain.endswith(cortVideo[j]) or contain.endswith(cortText[j]) or contain.endswith(cortMusic[j]) or contain.endswith(cortArchive[j]) or contain.endswith(cortVarious[j])):
                j += 1
            else:
                if contain.endswith(cortImage[j]):
                    dictFiles[cortImage].append(contain)
                elif contain.endswith(cortVideo[j]):
                    dictFiles[cortVideo].append(contain)
                elif contain.endswith(cortText[j]):
                    dictFiles[cortText].append(contain)
                elif contain.endswith(cortMusic[j]):
                    dictFiles[cortMusic].append(contain)
                elif contain.endswith(cortArchive[j]):
                    dictFiles[cortArchive].append(contain)
                elif contain.endswith(cortVarious[j]):
                    dictFiles[cortVarious].append(contain)
        elif pathlib.Path(contain).is_dir() and  not (contain == "images" or contain == "video" or contain == "documents" or contain == "audio" or contain == "archives" or contain == "other"):
            dictFiles[cortFolder].append(contain)
            sub_dir, newpath = inputing(path = pathlib.Path(contain).absolute())
            dictFiles[cortFolder].append(sorting(sub_dir, newpath))
            os.chdir(oldpath)
    return dictFiles

def normalize(my_string):

    alphabet_rus = ("а","б","в","г","д","е","ё","ж","з","и","й","к","л","м","н","о","п","р","с","т","у","ф","х","ц","ч","ш","щ","ъ","ы","ь","э","ю","я")
    alphabet_rus_eng = ("a","b","v","g","d","ye","yo","zh","z","i","j","k","l","m","n","o","p","r","s","t","u","f","kh","ts","ch","sh","shch","_","y","_","e","yu","ya")
    alphabet_ukr = ("а","б","в","г","ґ","д","е","є","ж","з","и","і","ї","й","к","л","м","н","о","п","р","с","т","у","ф","х","ц","ч","ш","щ","ь","ю","я")
    alphabet_ukr_eng = ("a", "b", "v", "h", "g", "d", "e", "ye", "zh", "z", "y", "i", "yi", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "kh", "ts", "ch", "sh", "shch", "_", "yu", "ya")
    
    map_trans = dict()
    for index, _ in enumerate(alphabet_rus):
        map_trans[ord(alphabet_rus[index])] = alphabet_rus_eng[index]
        map_trans[ord(alphabet_rus[index].upper())] = alphabet_rus_eng[index].capitalize()
        map_trans[ord(alphabet_ukr[index])] = alphabet_ukr_eng[index]
        map_trans[ord(alphabet_ukr[index].upper())] = alphabet_ukr_eng[index].capitalize()
    for symbol in string.punctuation:
        map_trans[ord(symbol)] = "_"
    for symbol in string.whitespace:
        map_trans[ord(symbol)] = "_"
    my_string = my_string.translate(map_trans)

    return my_string

def copyring(dictFiles, path_parent, path_destination):
    for key, lisf_of_files in dictFiles.items():
        new_dictFiles = dict()
        new_path = ""
        for a_file in lisf_of_files:
            if key == cortImage:
                os.chdir(f"{path_destination}/images")
                new_file_name = a_file.rsplit(".", 1)
                shutil.copyfile(path_parent + "/" + a_file, normalize(new_file_name[0]) + "." + new_file_name[1])
            if key == cortVideo:
                os.chdir(f"{path_destination}/video")
                new_file_name = a_file.rsplit(".", 1)
                shutil.copyfile(path_parent + "/" + a_file, normalize(new_file_name[0]) + "." + new_file_name[1])
            if key == cortText:
                os.chdir(f"{path_destination}/documents")
                new_file_name = a_file.rsplit(".", 1)
                shutil.copyfile(path_parent + "/" + a_file, normalize(new_file_name[0]) + "." + new_file_name[1])
            if key == cortMusic:
                os.chdir(f"{path_destination}/audio")
                new_file_name = a_file.rsplit(".", 1)
                shutil.copyfile(path_parent + "/" + a_file, normalize(new_file_name[0]) + "." + new_file_name[1])
            if key == cortArchive:
                new_file_name = a_file.rsplit(".", 1)
                shutil.unpack_archive(path_parent + "/" + a_file, path_destination + "/archives/" + normalize(new_file_name[0]))
            if key == cortVarious:
                os.chdir(f"{path_destination}/other")
                shutil.copyfile(path_parent + "/" + a_file, a_file)
            if key == cortFolder:
                if type(a_file) == type(str(a_file)):
                    new_path = path_parent + "/" + a_file
                elif type(a_file) == type(dict(a_file)):
                    new_dictFiles = a_file
                    copyring(new_dictFiles, new_path, path_destination)

def moving(dictFiles, path_parent, path_destination):
    for key, lisf_of_files in dictFiles.items():
        new_dictFiles = dict()
        new_path = ""
        for a_file in lisf_of_files:
            if key == cortImage:
                os.chdir(f"{path_destination}/images")
                new_file_name = a_file.rsplit(".", 1)
                shutil.move(path_parent + "/" + a_file, normalize(new_file_name[0]) + "." + new_file_name[1])
            if key == cortVideo:
                os.chdir(f"{path_destination}/video")
                new_file_name = a_file.rsplit(".", 1)
                shutil.move(path_parent + "/" + a_file, normalize(new_file_name[0]) + "." + new_file_name[1])
            if key == cortText:
                os.chdir(f"{path_destination}/documents")
                new_file_name = a_file.rsplit(".", 1)
                shutil.move(path_parent + "/" + a_file, normalize(new_file_name[0]) + "." + new_file_name[1])
            if key == cortMusic:
                os.chdir(f"{path_destination}/audio")
                new_file_name = a_file.rsplit(".", 1)
                shutil.move(path_parent + "/" + a_file, normalize(new_file_name[0]) + "." + new_file_name[1])
            if key == cortArchive:
                new_file_name = a_file.rsplit(".", 1)
                shutil.unpack_archive(path_parent + "/" + a_file, path_destination + "/archives/" + normalize(new_file_name[0]))
                os.remove(path_parent + "/" + a_file)
            if key == cortVarious:
                os.chdir(f"{path_destination}/other")
                shutil.move(path_parent + "/" + a_file, a_file)
            if key == cortFolder:
                if type(a_file) == type(str(a_file)):
                    new_path = path_parent + "/" + a_file
                elif type(a_file) == type(dict(a_file)):
                    new_dictFiles = a_file
                    moving(new_dictFiles, new_path, path_destination)

def creating_dir(path_destination):
    os.makedirs(f"{path_destination}/images", exist_ok = True)
    os.makedirs(f"{path_destination}/video", exist_ok = True)
    os.makedirs(f"{path_destination}/documents", exist_ok = True)
    os.makedirs(f"{path_destination}/audio", exist_ok = True)
    os.makedirs(f"{path_destination}/archives", exist_ok = True)
    os.makedirs(f"{path_destination}/other", exist_ok = True)

def deleting_space_dir(path_destination):
    contains = os.listdir(path_destination)
    if contains == []:
        os.removedirs(path_destination)
    else:
        os.chdir(path_destination)
    for contain in contains:
        if pathlib.Path(contain).is_dir() and  not (contain == "images" or contain == "video" or contain == "documents" or contain == "audio" or contain == "archives" or contain == "other"):
            deleting_space_dir(pathlib.Path(contain).absolute())
            if pathlib.Path(path_destination).exists():
                os.chdir(path_destination)

def main(path):

    contains, oldpath = inputing(path)

    dictFiles = sorting(contains, oldpath)

    while True:
        answer = input("\nif You wanna output the data on the screen or to record the data on the disk, enter please: 'screen', 'copy', 'move' or 'exit'\t")
        if answer == "screen":
            outputing(dictFiles)
        elif answer == "copy":
            creating_dir(oldpath)
            print("\n\tcopyring data (please wait) ... \n")
            copyring(dictFiles, oldpath, oldpath)
            print("\n\tdeleting space folders (please wait) ... \n")
            deleting_space_dir(oldpath)
        elif answer == "move":
            creating_dir(oldpath)
            print("\n\tmoving data (please wait) ... \n")
            moving(dictFiles, oldpath, oldpath)
            print("\n\tdeleting space folders (please wait) ... \n")
            deleting_space_dir(oldpath)
        elif answer == "exit":
            break
        else:
            print("\nYou maked the fail, reenter please.")

    print("\n\tWell done! Good luck You!\n")

if __name__ == "__main__":
    main()
