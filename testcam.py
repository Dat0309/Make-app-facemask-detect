import cv2 as cv

cap = cv.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    if(ret == True):
        cv.imshow('frame', frame)

        if cv.waitKey(20) & 0XFF == ord('q'):
            break

cap.release()
cv.destroyAllWindows()