import sys #Libreria para usar los argumentos de la linea de comando
tuplas=[]
archivo = sys.argv[1]
#archivo = "apila1.ap"
def noTerminal(a,b,c):
    rule=  "<"+a+","+b+","+c+">"
    if rule not in tuplas:
        tuplas.append(rule)
    return rule

aceptacion=[]
transiciones=[]
estados=[]
pila=[]

#Leer el contenido del AP a analizar 
#f = open(sys.argv[1], "r")
f = open(archivo, "r")
for transicion in f:
    if "inicial" in transicion:
        inicial=transicion.replace("\n","").split('=')[1] 
    elif "aceptacion" in transicion:
        aceptacion =transicion.replace("\n","").split('=')[1].split(",")
    else:
        transiciones.append(transicion.replace("\n","").replace(";",",").split(','))

#Obtenemos el conjunto de estados y simbolos de pila
for transicion in transiciones:
    if transicion[0] not in estados:
        estados.append(transicion[0])
    if transicion[3] not in estados:
        estados.append(transicion[3])
    if transicion[2] not in pila:
        pila.append(transicion[2])
    if transicion[4] not in pila:
        pila.append(transicion[4])
        
if "/" not in pila:
    pila.append("/")
    
reglasCFG=[]

#Paso 1
for estado  in aceptacion:
    reglasCFG.append(["S",noTerminal(inicial,"/",estado)])
    
#Paso 2
for estado in estados:
      reglasCFG.append([noTerminal(estado,"/",estado),"/"])
      
#Paso 3
for transicion in transiciones:
    if transicion[2]!="/":
        for estado in estados:
            reglasCFG.append([noTerminal(transicion[0],transicion[2],estado),transicion[1]+noTerminal(transicion[3],transicion[4],estado)])
#Paso 4
for transicion in transiciones:
    if transicion[2]=="/":
        for simbolo in pila:
            for estado1 in estados:
                for estado2 in estados:
                    reglasCFG.append(
                        [noTerminal(transicion[0],simbolo,estado1),
                        transicion[1]+noTerminal(transicion[3],transicion[4],estado2)+
                        noTerminal(estado2,simbolo,estado1)
                        ]
                     )
         
#Impresión de la CFG
file = open(archivo.split(".")[0]+".cfg","w") 
for regla in reglasCFG:
    print(regla[0]+"->"+regla[1])
    file.write(regla[0]+"->"+regla[1]+"\n")
file.close() 

#Sustitución de 3-tuplas de los no terminales de la FCG
for noTerm in tuplas:
    simbNoTerm= chr(tuplas.index(noTerm)+65)
    if simbNoTerm == "S":
        simbNoTerm="$"
    for i, regla in enumerate(reglasCFG):
        for j, elem in enumerate(reglasCFG[i]):
            reglasCFG[i][j]=reglasCFG[i][j].replace(noTerm,simbNoTerm)
            
#Impresión de la CFG con sustitución de 3-tuplas
if(len(tuplas)<27):
    file = open(archivo.split(".")[0]+"_min.cfg","w") 
    for regla in reglasCFG:
        print(regla[0]+"->"+regla[1])
        file.write(regla[0]+"->"+regla[1]+"\n")
    file.close() 
