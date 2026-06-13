import cv2
import numpy as np

video = cv2.VideoCapture('carros.MOV')
contador = 0
liberado = False

while True:
    ret,img = video.read()

    # por algum motivo o vídeo começa por padrão virado, 
    # por isso estou virando o vídeo em 90 graus
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    #resize
    img = cv2.resize(img,(720,1100),)

    imgGray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

    ## medidas do retangulo
    x,y,w,h = 300,530,40,80
  

    imgTh = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 12)
    kernel = np.ones((3,3), np.uint8)
    imgDil = cv2.dilate(imgTh,kernel,iterations=1)

    recorte = imgDil[y:y+h,x:x+w]
    brancos = cv2.countNonZero(recorte)

    ## contagem em si funcionando
    # 10 veiculos passam pelo video (logo esse é o objetivo) 
    if brancos > 2700 and liberado:
        contador +=1
        liberado = False
    if brancos < 2500:
        liberado = True

    if liberado == False:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)        
    else:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255, 0, 255),4)

    ## 
    cv2.putText(img,str(brancos),(x-30,y-60),cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),1)

    #contador dos carros/movimento
    cv2.putText(img, str(contador), (x+100, y), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 5)
    
    ## verificando os valores e a contagem 
    print(
        "brancos:",
        brancos,
        "liberado:",
        liberado,
        "contador:",
        contador
    )

    cv2.imshow('video original',img)

    if not ret:
        break

    # apertar esc se quiser fechar o vídeo a qualquer momento
    if cv2.waitKey(1) & 0xFF == 27:
        break