from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',
)

dialog_history = []



def menu(dialog_history):
    neurokeys = {}
    with open('models.txt') as f:
        c = 1
        for el in f.readlines():
            neurokeys[c] = str(el[:-1])
            c+= 1
    print('[0] - DataSet Mode')        
    for key in neurokeys.keys():
        print(f'[{key}] {neurokeys[key]}')
    
    s = int(input("Выберите функцию/нейросеть:"))
    if s == 0:
        for key in neurokeys.keys():
            print(f'[{key}] {neurokeys[key]}')
        s = int(input("Выберите нейросеть:"))
        print(f'Нейросеть {neurokeys[s]} готова к работе')
        return dataset(neurokeys[s], dialog_history)        
        
    else:
        print(f'Нейросеть {neurokeys[s]} готова к работе')
        return inwork(neurokeys[s], dialog_history)

def dataset(neuro,dialog_history):
    with open('dataset.txt') as f:
        for i in f.readlines():
            user_input = i
            if user_input.lower() == "/bye":
              
                    for el in dialog_history:
                        file_name = neuro.split(':')[0]
                        try:
                            
                            f = open(f'{file_name}.txt','a')
                            f.write(f'{el["role"]}: {el["content"]}\n')
                            f.close()
                        
                        except(UnicodeEncodeError):
                            f = open(f'{file_name}.txt','a')
                            f.write(f'{el["role"]}: encode error!!!\n')
                            f.close()                        
                            
                            
                    f = open(f'{file_name}.txt','a')
                    f.write(f'***конец сессии***\n')
                    f.close()            
                    dialog_history = []
                    return menu(dialog_history)
        
            
            dialog_history.append({
                "role": "user",
                "content": user_input,
            })
           
            
            response = client.chat.completions.create(
                model=neuro,
                messages=dialog_history,
            )
        
            
            response_content = response.choices[0].message.content
        
            print("Neuro:", response_content)
        
           
            dialog_history.append({
                "role": neuro,
                "content": response_content,
            })
                        

def inwork(neuro,dialog_history):
    while True:
        user_input = input("Введите ваше сообщение ('/bye' для завершения): ")
    
        if user_input.lower() == "/bye":
          
                for el in dialog_history:
                    file_name = neuro.split(':')[0]
                    try:
                        
                        f = open(f'{file_name}.txt','a')
                        f.write(f'{el["role"]}: {el["content"]}\n')
                        f.close()
                    
                    except(UnicodeEncodeError):
                        f = open(f'{file_name}.txt','a')
                        f.write(f'{el["role"]}: encode error!!!\n')
                        f.close()                        
                        
                        
                f = open(f'{file_name}.txt','a')
                f.write(f'***конец сессии***\n')
                f.close()            
                dialog_history = []
                return menu(dialog_history)
    
        
        dialog_history.append({
            "role": "user",
            "content": user_input,
        })
       
        
        response = client.chat.completions.create(
            model=neuro,
            messages=dialog_history,
        )
    
        
        response_content = response.choices[0].message.content
    
        print("Neuro:", response_content)
    
       
        dialog_history.append({
            "role": neuro,
            "content": response_content,
        })
        

menu(dialog_history)