import nltk

def view_samples(split_text, n=10):
    """ 
        Просмотр части разбитого на предложения датасета 
        n - кол-ко примеров
        split_text - датасет разбитый на предложения 
    """
    
    for i in split_text[0:n]:
        print('________________________________')
        print(i)
def replace(string, arrayoftrash):
    for i in arrayoftrash:
        string = string.replace(i,' ')
    return string 

def clear_text(filename, outfilename):
    """
        Чистка датасета от мусора и разбивка его на массив
        filename - имя файла
        outfilename - имя выходного файла
        Возвращает массив предложений 
    """
    
    with open(filename, 'r') as f:
        text = f.read()
    split_text = nltk.sent_tokenize(text)
    diction = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    trash = ['!','@','#','№','$',';','%','^',':','&','?','*','(',')','-','_','=','+','}','{','[',']','*','/','0','1','2','3','4','5','6','7','8','9',',']
    for i,item in enumerate(split_text):
        split_text[i] = replace(split_text[i], trash).lower()
        string = ''
        for char in split_text[i]:
            if char in diction or char == ' ':
                string += char
        split_text[i] = string
    with open(outfilename, 'a', encoding='utf-8') as out:
        for str in split_text:
            out.write(str + '\n')
    return split_text
    

