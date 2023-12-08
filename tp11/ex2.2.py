import multiprocessing as mp
import random

#only multiprocessing
def calculateur(output1, input2, i, sem):
        sem.acquire()
        data = output1.recv()
        sem.release()
        print(data)
        if (data[1] == "+"):
            calcul =int(data[0]) + int(data[2])
        elif (data[1] == "-"):
            calcul = int(data[0]) - int(data[2])
        elif (data[1] == "*"):
            calcul = int(data[0]) * int(data[2])
        elif (data[1] == "/"):
            calcul = int(data[0]) / int(data[2])
        input2.send(calcul)

def demandeur(output2, input1, i, sem):
        valeur_utilisateur1 = random.randint(0, 9)
        valeur_utilisateur2 = random.randint(0, 9)
        operations = ["+", "-", "*", "/"]
        signe = random.choice(operations)

        input1.send((valeur_utilisateur1, signe, valeur_utilisateur2))
        sem.acquire()
        data = output2.recv()
        sem.release()
        print("result " + str(data) + " de : " + str(i))

if __name__ == "__main__":
    process1 = []
    process2 = []
    output1,input1 = mp.Pipe()
    number = 5
    sem = mp.Lock() #initialisation 

    for i in range (number):
        output2,input2 = mp.Pipe()
        process1.append(mp.Process(target=calculateur, args=(output1, input2, i, sem)))
        process1[i].start()

        process2.append(mp.Process(target=demandeur, args=(output2, input1, i, sem)))
        process2[i].start()

    for i in range (number):
        process1[i].join()
        process2[i].join()
