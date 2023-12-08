import sys
import os
import multiprocessing as mp

#fork + multiprocessing
def forkAndMultiprocessing():
    output1,input1 = mp.Pipe()
    output2,input2 = mp.Pipe()
    pid = os.fork()
    if (pid == 0):
        while(True):
            data = output1.recv()
            print(data)
            if (data[1] == "+"):
                calcul =int(data[0]) + int(data[2])
            elif (data[1] == "-"):
                calcul = int(data[0]) - int(data[2])
            elif (data[1] == "*"):
                calcul = int(data[0]) * int(data[2])
            input2.send(calcul)
    else:
        while (True):
            valeur_utilisateur1 = input("Entrer la premiere valeur")
            signe = input("Entrer le signe du calcul")
            valeur_utilisateur2 = input("Entrer la deuxieme valeur")
            input1.send((valeur_utilisateur1, signe, valeur_utilisateur2))
            data = output2.recv()
            print("result " + str(data))





#only multiprocessing
def calculateur(output1, input2):
    while(True):
        data = output1.recv()
        print(data)
        if (data[1] == "+"):
            calcul =int(data[0]) + int(data[2])
        elif (data[1] == "-"):
            calcul = int(data[0]) - int(data[2])
        elif (data[1] == "*"):
            calcul = int(data[0]) * int(data[2])
        input2.send(calcul)

def demandeur(output2, input1):
    while (True):
        valeur_utilisateur1 = input("Entrer la premiere valeur")
        signe = input("Entrer le signe du calcul")
        valeur_utilisateur2 = input("Entrer la deuxieme valeur")
        input1.send((valeur_utilisateur1, signe, valeur_utilisateur2))
        data = output2.recv()
        print("result " + str(data))

if __name__ == "__main__":
    processList = []
    output1,input1 = mp.Pipe()
    output2,input2 = mp.Pipe()
    process1 = mp.Process(target=calculateur, args=(output1, input2))
    process1.start()
    demandeur(output2, input1)
    process1.join()
