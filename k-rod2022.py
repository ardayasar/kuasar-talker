# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 14:59:10 2021

@author: elif

başlangıçta servis olarak çalıştırdıysan eğer bu dosyayı monitorize etmek istersen servisi stopla veya öldür
  --> sudo systemctl stop krod.service
diğer iletişime geçtiği servislerden ise whitelist sürekli çalışmalı ki veri çeksin(internet bağlantısı kullanarak)

sidetalk.servie sistemi ise konuşma içindir oradaki ses bozukluğu durumunda kodlardan "aplay " olan satırı kontrol etmen gerek.

"""
from cv2 import destroyAllWindows, VideoCapture, resize, waitKey, rectangle, dnn, imshow, flip 
from numpy import argmax, array, tile
from datetime import datetime

def main(cap,cfg,weight):
    #"kamera karşısındaki nesnenin yön bilgisini ve nesne türünü bulur."
    

    while True:
        with open("waiting_for_talking.txt", "a") as file:
            file.write("Kırmızı:")
       # print("Sistem başlatıldı.")
        #t0=datetime.now()
        redline = 0
        ret, frame = cap.read()
    
        
        frame = resize(frame, (416, 416))
    
        #frame = flip(frame, 2)#filip edilmesine gerwek yok sağ sol isim değiştirmek yeterli.
        
        
        colors = ["0,255,255","0,255,0","255,0,0","255,255,0","0,255,0"]
        colors = [array(color.split(",")).astype("int") for color in colors]
        collors = array(colors)
        colors = tile(colors,(18,1))
    
        model = dnn.readNetFromDarknet(cfg, weight)
    
        #frame_width = frame.shape[1]
        frame_height , frame_width, _= frame.shape
    
        frame_blob = dnn.blobFromImage(frame, 1 / 255, (416, 416), swapRB=True, crop=False)
        #t1=datetime.now() hız testi
        #print("ilk işlem zamenı:",t1-t0)
        layers = model.getLayerNames()
        output_layer = [layers[layer[0] - 1] for layer in model.getUnconnectedOutLayers()]

        model.setInput(frame_blob)
    
        detection_layers = model.forward(output_layer)
    
        "############## NON-MAXIMUM SUPPRESSION - OPERATION 1 ###################"
    
        ids_list = []
        boxes_list = []
        confidences_list = []
    
        "############################ END OF OPERATION 1 ########################"
    
        for detection_layer in detection_layers:
            for object_detection in detection_layer:
    
                scores = object_detection[5:]
                predicted_id = argmax(scores)
                confidence = scores[predicted_id]
    
                if confidence > 0.30:
                    label = labels[predicted_id]
                    bounding_box = object_detection[0:4] * array([frame_width, frame_height, frame_width, frame_height])
                    (box_center_x, box_center_y, box_width, box_height) = bounding_box.astype("int")
    
                    start_x = int(box_center_x - (box_width / 2))
                    start_y = int(box_center_y - (box_height / 2))
    
                    "############## NON-MAXIMUM SUPPRESSION - OPERATION 2 ###################"
    
                    ids_list.append(predicted_id)
                    confidences_list.append(float(confidence))
                    boxes_list.append([start_x, start_y, int(box_width), int(box_height)])
    
                "############################ END OF OPERATION 2 ########################"
    
        "############## NON-MAXIMUM SUPPRESSION - OPERATION 3 ###################"
    
        max_ids = dnn.NMSBoxes(boxes_list, confidences_list, 0.5, 0.4)
    
        for max_id in max_ids:
    
            max_class_id = max_id[0]
            box = boxes_list[max_class_id]
    
            start_x = box[0]
            start_y = box[1]
            box_width = box[2]
            box_height = box[3]
     
            predicted_id = ids_list[max_class_id]
            label = labels[predicted_id]
            confidence = confidences_list[max_class_id]
    
            "############################ END OF OPERATION 3 ########################"
    
            end_x = start_x + box_width
            end_y = start_y + box_height
            
            box_color = colors[predicted_id]
            box_color = [int(each) for each in box_color]
            
            if end_y >= a:
                print("kırmızı alan uyarısı! {}".format(label))
                with open("waiting_for_talking.txt", "a") as file:
                    file.write("Kırmızı: {}".format(label))
        
                if end_x >= 278:
                    print("sol")
                    with open("waiting_for_talking.txt", "a") as file:
                        file.write("R- {}".format(label))
                elif 1 < end_x < 278:
                    print("sağ")
                    with open("waiting_for_talking.txt", "a") as file:
                        file.write("L- {}".format(label))
            else:
                print("-->")
    
            label = "{}: {:.2f}%".format(label, confidence * 100)
            print("predicted object {}".format(label))
            
            rectangle(frame, (start_x,start_y),(end_x,end_y),box_color,1)
    
        if waitKey(1) & ord("q") == 27:
            
            break
        #test amaçlı aç
        #imshow("Detector", frame)
    
    # %%
    cap.release()
    destroyAllWindows()

if __name__ == "__main__":
    
    cap = VideoCapture(0)
    
    dtw = open("/home/pi/Desktop/Kuasar_project/Artificial_Intelligense/data/waiting_for_talking.txt", "w")
    dtw.write('Test Panel')
    
    #mobil den alacağı veri için
    #ka = open("ka.txt")
    #c = ka.read()
    #a = int(c)
    #print(a)
    #ka.close()
    
    
    a=378
    cfg = "yolov4-tiny.cfg"
    weight = "yolov4-tiny_final.weights"
    
    #rectangle(frame, (0, 478), (638, a), (0, 0, 255), thickness=2)#gerçek sistemde bu satırların çalışmasına gerek yok.
    #rectangle(frame, (320, 478), (637, 0), (72, 155, 12), thickness=2)  # sag
    
    labels = ["insan"]
    
    main(cap,cfg,weight)

