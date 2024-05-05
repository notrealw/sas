import requests
import re
from colorama import init, Fore
import json
import os
from time import sleep
import ctypes

init(autoreset=True)

ctypes.windll.kernel32.SetConsoleTitleW("SAS FVCKER [Version 1.0.0]")

os.system("cls")
class SASFvcker:
    def __init__(self):
        with open('config.json', 'r') as arquivo_json:
            self.dados = json.load(arquivo_json)
        self.AUTH = self.dados["auth"]
        self.oldassignmentid = self.dados["assignmentid"]
        self.letras = ["A", "B", "C", "D"]
        self.s = requests.Session()
        self.headers = {"authorization": self.AUTH}

    def getauth(self):
        print("dsjahdakj")

    def getassignmentid(self, link):
        regex = r"/questionnaires/([^/]+)/question"
        id = re.search(regex, link).group(1)
        response = self.s.get(url=f"https://assignment-backend.sasdigital.com.br/questionnaires/{id}/assignments", headers=self.headers).json()
        return response["assignment"]["code"]

    def getquestionid(self, id):
        response = self.s.get(url=f"https://assignment-backend.sasdigital.com.br/questionnaires/{id}/assignments", headers=self.headers).json()
        return response["id"]

    def config(self):
        print(Fore.BLUE + """
███████╗ █████╗ ███████╗    ███████╗██╗   ██╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔════╝██╔══██╗██╔════╝    ██╔════╝██║   ██║██╔════╝██║ ██╔╝██╔════╝██╔══██╗
███████╗███████║███████╗    █████╗  ██║   ██║██║     █████╔╝ █████╗  ██████╔╝
╚════██║██╔══██║╚════██║    ██╔══╝  ╚██╗ ██╔╝██║     ██╔═██╗ ██╔══╝  ██╔══██╗
███████║██║  ██║███████║    ██║      ╚████╔╝ ╚██████╗██║  ██╗███████╗██║  ██║
╚══════╝╚═╝  ╚═╝╚══════╝    ╚═╝       ╚═══╝   ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                             
             ██████╗ ██████╗ ███╗   ██╗███████╗██╗ ██████╗                   
            ██╔════╝██╔═══██╗████╗  ██║██╔════╝██║██╔════╝                   
            ██║     ██║   ██║██╔██╗ ██║█████╗  ██║██║  ███╗                  
            ██║     ██║   ██║██║╚██╗██║██╔══╝  ██║██║   ██║                  
            ╚██████╗╚██████╔╝██║ ╚████║██║     ██║╚██████╔╝                  
             ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝                   
""")
        print(Fore.GREEN+ "Olá, bem-vindo! Foi notado que essa é sua primeira vez usando o SAS FVCKER, antes de prosseguir, é necessário que nos responda algumas perguntas. Mas pode ficar tranquilo, seus dados não serão enviados a lugar nenhum, apenas atribuidos ao seu banco de dados interno (config.json).")
        authinput = input("[>] Token De Autenticação Do Portal SAS: ")
        print("[...] Aguarde enquanto inserimos seu Token De Autenticação (AUTH) no banco de dados.")
        self.dados["auth"] = authinput
        self.AUTH = authinput
        self.headers = {"authorization": self.AUTH}
        with open('config.json', 'w') as arquivo_json:
            json.dump(self.dados, arquivo_json, indent=2)
        oldeureka = input("[>] Insira o link de um Eureka antigo que você já tenha feito ou que não importe mais: ")
        self.dados["assignmentid"] = self.getassignmentid(oldeureka)
        with open('config.json', 'w') as arquivo_json:
            json.dump(self.dados, arquivo_json, indent=2)
        self.oldassignmentid = self.getassignmentid(oldeureka)
        self.main()

    def getanswer(self, id):
        try:
            data = {
                "questionId": id,
                "markedOption": 1
            }
            response = self.s.post(url=f"https://assignment-backend.sasdigital.com.br/assignments/{self.oldassignmentid}/answers", headers=self.headers, json=data).json()
            answer = response["answer"]["correctOption"]
            return answer
        except Exception as erro:
            print(Fore.RED+ "[-] Vish. Parece que já está na hora de trocar o link de Eureka antigo!")
            newoldeureka = input("[>] Insira o link de um novo Eureka antigo: ")
            print("[...] Aguarde enquanto inserimos suas novas informações no banco de dados.")
            self.oldassignmentid = self.getassignmentid(newoldeureka)
            self.dados["assignmentid"] = self.getassignmentid(newoldeureka)
            with open('config.json', 'w') as arquivo_json:
                json.dump(self.dados, arquivo_json, indent=2)
            os.system("cls")
            self.main()

    def autoeureka(self, eureka):
        assignmentid = self.getassignmentid(eureka)
        canbefinished = self.s.get(url=f"https://assignment-backend.sasdigital.com.br/assignments/{assignmentid}/progress", headers=self.headers).json()["canBeFinished"]
        currentquestion = int(self.s.get(url=f"https://assignment-backend.sasdigital.com.br/assignments/{assignmentid}/progress", headers=self.headers).json()["current"])
        while currentquestion <= 12:
            regex = r"/questionnaires/([^/]+)/question"
            id = re.search(regex, eureka).group(1)
            questionid = self.getquestionid(id)
            canbefinished = self.s.get(url=f"https://assignment-backend.sasdigital.com.br/assignments/{assignmentid}/progress", headers=self.headers).json()["canBeFinished"]
            resposta = self.getanswer(questionid)
            data = {
                "questionId": questionid,
                "markedOption": resposta
            }
            response = self.s.post(url=f"https://assignment-backend.sasdigital.com.br/assignments/{assignmentid}/answers", headers=self.headers, json=data)
            if response.status_code in [200, 201]:
                print(Fore.GREEN + f"[+] Questão de ID {questionid} respondida! | Número: {currentquestion} | Alternativa Correta: {self.letras[resposta]}.")
                if currentquestion < 12:
                    self.s.get(f"https://assignment-backend.sasdigital.com.br/assignments/{assignmentid}/questions", headers=self.headers)
                    currentquestion += 1 
                if currentquestion == 12 and canbefinished == True:
                    response = self.s.put(f"https://assignment-backend.sasdigital.com.br/assignments/{assignmentid}", headers=self.headers, json={"status":"finished"}) #finalizar 1
                    print(Fore.GREEN+"[+] Capítulo finalizado!")
                    print(Fore.YELLOW+"------ made by @ravenfrombrazil")
                    input("[>] Pressione qualquer tecla para voltar ao menu incial... ")
                    os.system("cls")
                    self.main()
                    break

    def main(self):
        if self.AUTH == "" and self.oldassignmentid == "":
            self.config()
        print(Fore.BLUE+ """
███████╗ █████╗ ███████╗    ███████╗██╗   ██╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔════╝██╔══██╗██╔════╝    ██╔════╝██║   ██║██╔════╝██║ ██╔╝██╔════╝██╔══██╗
███████╗███████║███████╗    █████╗  ██║   ██║██║     █████╔╝ █████╗  ██████╔╝
╚════██║██╔══██║╚════██║    ██╔══╝  ╚██╗ ██╔╝██║     ██╔═██╗ ██╔══╝  ██╔══██╗
███████║██║  ██║███████║    ██║      ╚████╔╝ ╚██████╗██║  ██╗███████╗██║  ██║
╚══════╝╚═╝  ╚═╝╚══════╝    ╚═╝       ╚═══╝   ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
        """)

        print(Fore.BLUE+ f"""1) | Revelar Alternativa Correta
2) | Realizar Eureka
        """)

        option = int(input("[>] Selecione a opção que deseja utilizar: "))

        if option == 1:
            eureka = input("[>] Insira o link da questão: ")
            assignmentid = self.getassignmentid(eureka)
            questionid = self.getquestionid(assignmentid)
            resposta = self.getanswer(questionid)
            print(Fore.GREEN + f"[+] A resposta correta é: {self.letras[resposta]}.")
        elif option == 2:
            eureka = input("[>] Insira o link da questão: ")
            os.system("cls")
            print(Fore.BLUE+ """
███████╗ █████╗ ███████╗    ███████╗██╗   ██╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔════╝██╔══██╗██╔════╝    ██╔════╝██║   ██║██╔════╝██║ ██╔╝██╔════╝██╔══██╗
███████╗███████║███████╗    █████╗  ██║   ██║██║     █████╔╝ █████╗  ██████╔╝
╚════██║██╔══██║╚════██║    ██╔══╝  ╚██╗ ██╔╝██║     ██╔═██╗ ██╔══╝  ██╔══██╗
███████║██║  ██║███████║    ██║      ╚████╔╝ ╚██████╗██║  ██╗███████╗██║  ██║
╚══════╝╚═╝  ╚═╝╚══════╝    ╚═╝       ╚═══╝   ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
        """)

            print(Fore.BLUE + f"""1) | Revelar Alternativa Correta
2) | Realizar Eureka\n{Fore.YELLOW}------ made by @ravenfrombrazil""")
            self.autoeureka(eureka)
            os.system("cls")

sas_fvcker = SASFvcker()
sas_fvcker.main()