import numpy
import cv2
import cv2.aruco as aruco

# generates 500px images of aruco markers
def create_aruco():
	dictionary = aruco.getPredefinedDictionary(0)
	for boi in range(50):
		img = aruco.drawMarker(dictionary, boi, 500)
		cv2.imwrite("aruco_4x4_" + str(boi) + ".jpg", img)

cap = cv2.VideoCapture(0)

def detect_markers():
	while(True):
	    ret, frame = cap.read()

	    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	    aruco_dict = aruco.getPredefinedDictionary(0)
	    parameters =  aruco.DetectorParameters_create()

	    cv2.rectangle(frame, (50,50), (1230,670), (255,0,0),2 )

	    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
	    for box_index in range(len(corners)):
	    	x_avg = 0
	    	y_avg = 0 
	    	for x,y in corners[box_index][0]: # the box
	    		x_avg += x/4
	    		y_avg += y/4
	    	cv2.rectangle(frame, (int(x_avg),int(y_avg)), (int(x_avg+5),int(y_avg+5)), (0,255,0),2)
	    	cv2.putText(frame,"id="+str(ids[box_index])+" ("+str(int(x_avg))+","+str(int(y_avg))+")", (int(x_avg),int(y_avg)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))

	 
	    gray = aruco.drawDetectedMarkers(frame, corners)
	 
	    #print(rejectedImgPoints)
	    # Display the resulting frame
	    cv2.imshow('frame',frame)
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break

# def draw_grid(frame, row, col):
# 	for i in range(row):
# 		cv2.line(frame,)

# 	for j in range(col):


# def highlight_grid(frame, )


detect_markers()
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

